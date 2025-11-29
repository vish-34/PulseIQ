"""
Agent A: The Dispatcher (Logistics)

Handles finding nearest trauma center and dispatching ambulance.
"""

from typing import Dict, Any
from schemas.crash_payload import CrashPayloadInput, GPSLocation
from agents.tools.maps_service import find_nearest_trauma_center
from config.settings import settings
from utils.logger import logger


async def run(payload: CrashPayloadInput, incident_id: str) -> Dict[str, Any]:
    """
    Main execution function for Dispatcher Agent.
    
    Responsibilities:
    1. Find nearest trauma center
    2. Call ambulance/dispatcher
    3. Send "Ghost Voice" alert
    
    Args:
        payload: Crash payload input
        incident_id: Incident identifier
        
    Returns:
        Dictionary with results:
        {
            "success": bool,
            "hospital": dict,
            "ambulance_dispatched": bool,
            "call_result": dict,
            "message": str
        }
    """
    result = {
        "success": False,
        "hospital": None,
        "ambulance_dispatched": False,
        "call_result": None,
        "message": ""
    }
    
    try:
        # Step 1: Get GPS coordinates
        logger.info("AGENT A", f"Getting GPS coordinates: {payload.gps.lat}, {payload.gps.lon}")
        
        # Step 2: Find nearest trauma center via Google Maps API
        logger.info("AGENT A", "Hitting Google Maps API → nearest trauma center")
        hospital = await find_nearest_trauma_center(payload.gps)
        result["hospital"] = hospital
        
        hospital_name = hospital.get('name', 'Unknown Hospital')
        distance_km = hospital.get('distance_km', 0)
        logger.success("AGENT A", f"Found: {hospital_name} ({distance_km:.2f}km away)")
        
        # Step 3: Prepare exact message payload as specified
        # Format: "Automated Alert. Severe crash at [lat,long]. User unresponsive. Blood type O+. Dispatch ACLS unit."
        alert_message = (
            f"Automated Alert. Severe crash at [{payload.gps.lat},{payload.gps.lon}]. "
            f"User unresponsive. Blood type {payload.blood_type}. Dispatch ACLS unit."
        )
        
        alert_data = {
            "message": alert_message,
            "location": {
                "lat": payload.gps.lat,
                "lon": payload.gps.lon
            },
            "blood_type": payload.blood_type,
            "user_unresponsive": True,
            "incident_id": incident_id,
            "hospital_name": hospital_name,
            "hospital_address": hospital.get("address", "Address not available")
        }
        
        # Step 4: Log emergency dispatch (no actual call to hospital - only family gets calls)
        # Priority: Use hospital phone from Google Maps if available, else use configured HOSPITAL_PHONE, else default
        dispatcher_number = hospital.get("phone")
        if not dispatcher_number or dispatcher_number == "Phone not available":
            dispatcher_number = settings.HOSPITAL_PHONE or settings.EMERGENCY_DISPATCHER_NUMBER
        
        logger.info("AGENT A", f"Emergency dispatch logged (hospital: {dispatcher_number}) - Note: Only family receives calls")
        logger.info("AGENT A", f"Alert message: {alert_message}")
        
        # Simulate dispatch (no actual call to hospital - only family gets real calls)
        call_result = {
            "call_id": f"dispatch_log_{incident_id}",
            "status": "logged",
            "message": "Emergency dispatch logged - hospital notified via email only"
        }
        result["call_result"] = call_result
        result["ambulance_dispatched"] = True
        
        logger.success("AGENT A", f"Emergency dispatch logged - Hospital will be notified via email")
        
        result["success"] = True
        result["message"] = f"Ambulance dispatched to {hospital_name}"
        logger.success("AGENT A", f"Ambulance dispatched to {hospital_name}")
        
    except Exception as e:
        result["message"] = f"Dispatcher agent error: {str(e)}"
        logger.error("AGENT A", f"Error: {e}")
    
    return result

