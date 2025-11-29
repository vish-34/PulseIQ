"""
Verify Google Maps API Setup - Check if API key is working
"""

import asyncio
import sys
import os
from pathlib import Path

# Change to backend/src directory to load .env correctly
backend_src = Path(__file__).parent / 'backend' / 'src'
os.chdir(backend_src)
sys.path.insert(0, str(backend_src))

from config.settings import settings
import httpx


async def verify_api_key():
    """Verify Google Maps API key is working"""
    
    print("="*70)
    print("VERIFYING GOOGLE MAPS API SETUP")
    print("="*70)
    print()
    
    # Check if API key exists
    if not settings.GOOGLE_MAPS_API_KEY:
        print("ERROR: GOOGLE_MAPS_API_KEY not found in .env file")
        print("   Add your API key to backend/src/.env")
        return False
    
    api_key = settings.GOOGLE_MAPS_API_KEY
    print(f"API Key found: {api_key[:20]}...{api_key[-10:]}")
    print()
    
    # Test with a simple Places API request
    print("Testing Places API with NESCO Centre Goregaon location...")
    print("Location: 19.1680, 72.8500")
    print()
    
    try:
        async with httpx.AsyncClient() as client:
            url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
            params = {
                "location": "19.1680,72.8500",
                "radius": 5000,  # 5km radius
                "type": "hospital",
                "key": api_key
            }
            
            print("Making API request...")
            response = await client.get(url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            status = data.get("status")
            print(f"API Response Status: {status}")
            print()
            
            if status == "OK":
                results = data.get("results", [])
                print(f"SUCCESS! Found {len(results)} hospitals")
                print()
                if results:
                    print("Nearest hospitals:")
                    for i, hospital in enumerate(results[:5], 1):
                        name = hospital.get("name", "Unknown")
                        vicinity = hospital.get("vicinity", "Address not available")
                        print(f"  {i}. {name}")
                        print(f"     Address: {vicinity}")
                        print()
                return True
            elif status == "REQUEST_DENIED":
                error_msg = data.get("error_message", "")
                print("REQUEST_DENIED")
                print(f"Error: {error_msg}")
                print()
                print("Possible issues:")
                print("  1. Places API not enabled in Google Cloud Console")
                print("  2. Billing not enabled (even for free tier)")
                print("  3. API key restrictions blocking the request")
                print("  4. API key is invalid or from wrong project")
                print()
                print("Fix:")
                print("  1. Go to: https://console.cloud.google.com/apis/library")
                print("  2. Search for 'Places API' and enable it")
                print("  3. Go to: https://console.cloud.google.com/project/_/billing/enable")
                print("  4. Enable billing (required even for free tier)")
                return False
            elif status == "INVALID_REQUEST":
                error_msg = data.get("error_message", "")
                print("INVALID_REQUEST")
                print(f"Error: {error_msg}")
                return False
            elif status == "ZERO_RESULTS":
                print("ZERO_RESULTS - No hospitals found in the area")
                print("   This might be normal if the area has no hospitals")
                return True  # API is working, just no results
            else:
                error_msg = data.get("error_message", "")
                print(f"Status: {status}")
                if error_msg:
                    print(f"Error: {error_msg}")
                return False
                
    except Exception as e:
        print(f"Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(verify_api_key())
    if success:
        print("="*70)
        print("SUCCESS: Google Maps API is working correctly!")
        print("   The system will find real hospitals near NESCO Centre Goregaon")
        print("="*70)
    else:
        print("="*70)
        print("ERROR: Google Maps API setup needs attention")
        print("   Follow the instructions above to fix the issue")
        print("="*70)

