"""
Hospital Arrival Geofencing

Monitors GPS coordinates to detect when user arrives at hospital.
Implements Phase 3: Hospital Arrival Handoff
"""

import math
from typing import Dict, Any, Optional
from schemas.crash_payload import GPSLocation
from config.settings import settings
from utils.logger import logger
from agents.tools.email_service import send_family_notification
from utils.black_box import stop_black_box_recording
from agents.core.state_machine import IncidentState


def calculate_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate distance between two GPS coordinates using Haversine formula.
    
    Args:
        lat1, lon1: First GPS coordinates
        lat2, lon2: Second GPS coordinates
        
    Returns:
        Distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)
    
    # Haversine formula
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    a = math.sin(dlat / 2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance


def check_hospital_arrival(
    current_gps: GPSLocation,
    hospital_gps: GPSLocation,
    threshold_meters: Optional[float] = None
) -> bool:
    """
    Check if current GPS matches hospital GPS geofence.
    
    Args:
        current_gps: Current device GPS coordinates
        hospital_gps: Hospital GPS coordinates
        threshold_meters: Distance threshold in meters (default from settings)
        
    Returns:
        True if within threshold, False otherwise
    """
    threshold = threshold_meters or (settings.HOSPITAL_ARRIVAL_THRESHOLD_METERS * 1000)  # Convert to meters
    
    distance_km = calculate_distance_km(
        current_gps.lat, current_gps.lon,
        hospital_gps.lat, hospital_gps.lon
    )
    distance_meters = distance_km * 1000
    
    logger.info("GEOFENCE", f"Distance to hospital: {distance_meters:.2f}m (threshold: {threshold:.2f}m)")
    
    return distance_meters <= threshold


async def handle_hospital_arrival(
    incident_id: str,
    incident_state: IncidentState,
    hospital_gps: GPSLocation,
    hospital_name: str = "Trauma Center"
) -> Dict[str, Any]:
    """
    Handle Phase 3: Hospital Arrival Handoff.
    
    When device GPS matches hospital geofence:
    1. Switch to Hospital Mode
    2. Stop Black Box mode
    3. Notify family: "User has reached the trauma center. Stabilization in progress."
    
    Args:
        incident_id: Incident identifier
        incident_state: State machine instance
        hospital_gps: Hospital GPS coordinates
        hospital_name: Hospital name
        
    Returns:
        Dictionary with handoff results
    """
    logger.info("PHASE_3", "Hospital Arrival Handoff initiated")
    
    result = {
        "success": False,
        "hospital_mode_activated": False,
        "black_box_stopped": False,
        "family_notified": False,
        "message": ""
    }
    
    try:
        # Step 1: Switch to Hospital Mode
        if incident_state.enter_hospital_mode(hospital_gps):
            result["hospital_mode_activated"] = True
            logger.success("PHASE_3", f"Hospital Mode activated - GPS match at {hospital_gps.lat}, {hospital_gps.lon}")
        else:
            logger.error("PHASE_3", "Failed to enter Hospital Mode")
            return result
        
        # Step 2: Stop Black Box mode
        logger.info("PHASE_3", "Stopping Black Box mode")
        from utils.black_box import stop_black_box_recording
        black_box_result = await stop_black_box_recording(incident_id)
        if black_box_result:
            result["black_box_stopped"] = True
            logger.success("PHASE_3", f"Black Box recording stopped: {black_box_result.get('recording_id')}")
        else:
            logger.warn("PHASE_3", "No active Black Box recording found")
        
        # Step 3: Notify family (email + call + SMS)
        logger.info("PHASE_3", "Notifying family: Hospital arrival update")
        from utils.family_notifications import notify_family_hospital_arrival
        
        family_notification_result = await notify_family_hospital_arrival(
            incident_id=incident_id,
            hospital_name=hospital_name,
            hospital_gps_lat=hospital_gps.lat,
            hospital_gps_lon=hospital_gps.lon
        )
        
        result["family_notified"] = family_notification_result.get("success", False)
        if result["family_notified"]:
            logger.success("PHASE_3", "Family hospital arrival notifications sent (email, call, SMS)")
        else:
            logger.warn("PHASE_3", "Family notification partially failed - check logs")
        
        result["success"] = True
        result["message"] = "Hospital arrival handoff completed"
        logger.success("PHASE_3", "✅ Hospital Arrival Handoff complete - All tasks finished")
        
    except Exception as e:
        result["message"] = f"Hospital arrival handoff error: {str(e)}"
        logger.error("PHASE_3", f"Error: {e}")
    
    return result

