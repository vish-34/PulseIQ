"""
Maps Service - Google Maps API Integration

Finds nearest trauma centers and provides location services.
"""

import httpx
from typing import Optional, Dict, Any
from schemas.crash_payload import GPSLocation
from config.settings import settings


async def find_nearest_trauma_center(gps: GPSLocation) -> Dict[str, Any]:
    """
    Find the nearest trauma center using Google Maps Places API.
    
    Args:
        gps: GPS coordinates of the crash location
        
    Returns:
        Dictionary containing hospital information:
        {
            "name": str,
            "address": str,
            "phone": str,
            "email": str,
            "gps": {"lat": float, "lon": float},
            "distance_km": float,
            "place_id": str
        }
    """
    if not settings.GOOGLE_MAPS_API_KEY:
        # Mock response for demo/testing
        return _mock_find_hospital(gps)
    
    try:
        async with httpx.AsyncClient() as client:
            # Nearby Search API
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": f"{gps.lat},{gps.lon}",
                "radius": 10000,  # 10km radius
                "type": "hospital",
                "keyword": "trauma center emergency",
                "key": settings.GOOGLE_MAPS_API_KEY
            }
            
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Log API response for debugging
            api_status = data.get("status")
            if api_status != "OK":
                print(f"Google Maps API Status: {api_status}")
                if api_status == "REQUEST_DENIED":
                    print(f"Error: {data.get('error_message', 'API key may be invalid or Places API not enabled')}")
                elif api_status == "ZERO_RESULTS":
                    print("No hospitals found in the area")
                else:
                    print(f"API Error: {data.get('error_message', 'Unknown error')}")
            
            if data.get("status") == "OK" and data.get("results"):
                # Get the nearest hospital (first result)
                place = data["results"][0]
                place_id = place["place_id"]
                
                # Get detailed information including phone and email
                details = await _get_place_details(place_id)
                
                # Calculate distance
                distance_km = _calculate_distance(
                    gps.lat, gps.lon,
                    place["geometry"]["location"]["lat"],
                    place["geometry"]["location"]["lng"]
                )
                
                # Get phone/email from Google Maps (for display/logging only)
                google_phone = details.get("formatted_phone_number")
                google_email = details.get("email")
                
                # ALWAYS use configured phone/email for actual notifications
                # Google Maps data is only for display/logging purposes
                hospital_phone = settings.HOSPITAL_PHONE or google_phone or "Phone not available"
                hospital_email = settings.HOSPITAL_EMAIL or google_email or f"emergency@{place.get('name', 'hospital').lower().replace(' ', '')}.com"
                
                return {
                    "name": place.get("name", "Unknown Hospital"),
                    "address": place.get("vicinity", details.get("formatted_address", "Address not available")),
                    "phone": hospital_phone,  # Always uses configured HOSPITAL_PHONE
                    "email": hospital_email,   # Always uses configured HOSPITAL_EMAIL
                    "gps": {
                        "lat": place["geometry"]["location"]["lat"],
                        "lon": place["geometry"]["location"]["lng"]
                    },
                    "distance_km": round(distance_km, 2),
                    "place_id": place_id,
                    "phone_from_google": google_phone is not None,
                    "email_from_google": google_email is not None,
                    "google_phone": google_phone,  # Store for reference
                    "google_email": google_email    # Store for reference
                }
            else:
                # Fallback to mock if API fails
                return _mock_find_hospital(gps)
                
    except Exception as e:
        # Fallback to mock on error
        error_type = type(e).__name__
        error_msg = str(e)
        print(f"Maps API error ({error_type}): {error_msg}")
        if "getaddrinfo failed" in error_msg or "11001" in error_msg:
            print("  → Network/DNS issue: Check internet connection")
        elif "REQUEST_DENIED" in error_msg:
            print("  → API issue: Enable Places API and billing in Google Cloud Console")
        print("  → Using mock hospital data")
        return _mock_find_hospital(gps)


async def _get_place_details(place_id: str) -> Dict[str, Any]:
    """Get detailed information about a place"""
    if not settings.GOOGLE_MAPS_API_KEY:
        return {}
    
    try:
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                "place_id": place_id,
                "fields": "formatted_address,formatted_phone_number,website,name",
                "key": settings.GOOGLE_MAPS_API_KEY
            }
            
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("result", {})
            else:
                # Log error for debugging
                error_status = data.get("status")
                error_msg = data.get("error_message", "")
                if error_status == "REQUEST_DENIED":
                    print(f"⚠️  Place Details API Error: {error_msg}")
                return {}
    except Exception as e:
        print(f"⚠️  Place Details API Exception: {e}")
        return {}
    
    return {}


async def get_directions(origin: GPSLocation, destination: GPSLocation) -> Dict[str, Any]:
    """
    Get directions from origin to destination.
    
    Args:
        origin: Starting GPS coordinates
        destination: Target GPS coordinates
        
    Returns:
        Dictionary containing:
        {
            "distance_km": float,
            "duration_minutes": float,
            "route": str (encoded polyline or summary)
        }
    """
    if not settings.GOOGLE_MAPS_API_KEY:
        # Mock response
        distance_km = _calculate_distance(origin.lat, origin.lon, destination.lat, destination.lon)
        return {
            "distance_km": round(distance_km, 2),
            "duration_minutes": round(distance_km * 2, 1),  # Assume 30 km/h average
            "route": "Mock route data"
        }
    
    try:
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/directions/json"
            params = {
                "origin": f"{origin.lat},{origin.lon}",
                "destination": f"{destination.lat},{destination.lon}",
                "key": settings.GOOGLE_MAPS_API_KEY
            }
            
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK" and data.get("routes"):
                route = data["routes"][0]
                leg = route["legs"][0]
                
                return {
                    "distance_km": round(leg["distance"]["value"] / 1000, 2),
                    "duration_minutes": round(leg["duration"]["value"] / 60, 1),
                    "route": route.get("summary", "Route available")
                }
    except Exception as e:
        print(f"Directions API error: {e}")
    
    # Fallback
    distance_km = _calculate_distance(origin.lat, origin.lon, destination.lat, destination.lon)
    return {
        "distance_km": round(distance_km, 2),
        "duration_minutes": round(distance_km * 2, 1),
        "route": "Route calculation unavailable"
    }


def _calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula.
    
    Returns distance in kilometers.
    """
    from math import radians, cos, sin, asin, sqrt
    
    # Convert to radians
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Earth radius in kilometers
    
    return c * r


def _mock_find_hospital(gps: GPSLocation) -> Dict[str, Any]:
    """
    Mock hospital finder for demo/testing when Google Maps API is not available.
    
    Uses real hospital data (Kokilaben Dhirubhai Ambani Hospital) for realistic demo.
    ALWAYS uses configured HOSPITAL_PHONE and HOSPITAL_EMAIL for notifications.
    """
    from config.settings import settings
    
    # ALWAYS use configured hospital phone/email (never use Google Maps data)
    hospital_phone = settings.HOSPITAL_PHONE or "+91-1234567890"
    hospital_email = settings.HOSPITAL_EMAIL or "emergency@citytrauma.com"
    
    # Real hospital near NESCO Centre Goregaon
    # Kokilaben Dhirubhai Ambani Hospital is approximately 2-3km from NESCO Centre
    # GPS coordinates: ~19.145, 72.830 (Andheri West)
    return {
        "name": "Kokilaben Dhirubhai Ambani Hospital",
        "address": "Four Bungalows, Andheri West, Mumbai",
        "phone": hospital_phone,  # Always uses configured
        "email": hospital_email,  # Always uses configured
        "gps": {
            "lat": 19.145,  # Approximate location of Kokilaben Hospital
            "lon": 72.830
        },
        "distance_km": round(_calculate_distance(gps.lat, gps.lon, 19.145, 72.830), 2),
        "place_id": "mock_kokilaben_hospital",
        "phone_from_google": False,
        "email_from_google": False,
        "google_phone": None,  # No Google data in mock
        "google_email": None   # No Google data in mock
    }

