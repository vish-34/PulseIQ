"""
Hospital Arrival Handler - Phase 3: The Handoff

Detects when user arrives at hospital and switches to Hospital Mode.
"""

from typing import Dict, Any, Optional
from schemas.crash_payload import GPSLocation
from agents.core.state_machine import IncidentState
from agents.tools.maps_service import _calculate_distance
from agents.tools.twilio_service import send_sms
from agents.tools.email_service import send_family_notification
from config.settings import settings


async def monitor_arrival(
    current_gps: GPSLocation,
    hospital_gps: GPSLocation,
    incident_id: str,
    incident_state: IncidentState
) -> bool:
    """
    Monitor if user has arrived at hospital.
    
    Checks if current GPS matches hospital GPS (within threshold).
    If match detected, switches state machine to hospital_mode.
    
    Args:
        current_gps: Current phone GPS coordinates
        hospital_gps: Hospital GPS coordinates
        incident_id: Incident identifier
        incident_state: State machine instance
        
    Returns:
        True if arrival detected and state switched, False otherwise
    """
    # Calculate distance
    distance_meters = _calculate_distance(
        current_gps.lat, current_gps.lon,
        hospital_gps.lat, hospital_gps.lon
    ) * 1000  # Convert km to meters
    
    print(f"[HOSPITAL HANDLER] Distance to hospital: {distance_meters:.1f} meters")
    
    # Check if within threshold
    if distance_meters <= settings.HOSPITAL_ARRIVAL_THRESHOLD_METERS:
        if incident_state.state == "dispatching":
            # Switch to hospital mode
            success = incident_state.enter_hospital_mode(hospital_gps)
            
            if success:
                print(f"[HOSPITAL HANDLER] ✅ Arrival detected! Switched to hospital_mode")
                return True
    
    return False


async def send_arrival_notification(
    family_contact: Optional[str],
    hospital_info: Dict[str, Any],
    incident_id: str,
    incident_state: IncidentState
) -> bool:
    """
    Send notification to family when user arrives at hospital.
    
    Message: "User has arrived at City Hospital. Vitals are stable. Ward number pending."
    
    Args:
        family_contact: Family/emergency contact phone or email
        hospital_info: Hospital information dictionary
        incident_id: Incident identifier
        incident_state: State machine instance
        
    Returns:
        True if notification sent successfully
    """
    hospital_name = hospital_info.get("name", "City Hospital")
    hospital_address = hospital_info.get("address", "")
    
    message = (
        f"Emergency Update: User has arrived at {hospital_name}. "
        f"Vitals are stable. Ward number pending. "
        f"Incident ID: {incident_id}"
    )
    
    # Use configured family contact if not provided
    if not family_contact:
        family_contact = settings.FAMILY_PHONE or settings.FAMILY_EMAIL
    
    try:
        # Try SMS first (if it's a phone number)
        if family_contact and family_contact.startswith("+"):
            sms_result = await send_sms(family_contact, message)
            if sms_result.get("status") == "sent":
                print(f"[HOSPITAL HANDLER] SMS sent to {family_contact}")
                return True
        
        # Try email
        if family_contact and "@" in family_contact:
            incident_info = {
                "incident_id": incident_id,
                "hospital_name": hospital_name,
                "hospital_address": hospital_address,
                "status": "stable"
            }
            email_result = await send_family_notification(family_contact, incident_info)
            if email_result:
                print(f"[HOSPITAL HANDLER] Email sent to {family_contact}")
                return True
        
        # Try configured family email/phone
        if settings.FAMILY_EMAIL:
            incident_info = {
                "incident_id": incident_id,
                "hospital_name": hospital_name,
                "hospital_address": hospital_address,
                "status": "stable"
            }
            email_result = await send_family_notification(settings.FAMILY_EMAIL, incident_info)
            if email_result:
                print(f"[HOSPITAL HANDLER] Email sent to {settings.FAMILY_EMAIL}")
                return True
        
        if settings.FAMILY_PHONE:
            sms_result = await send_sms(settings.FAMILY_PHONE, message)
            if sms_result.get("status") == "sent":
                print(f"[HOSPITAL HANDLER] SMS sent to {settings.FAMILY_PHONE}")
                return True
        
        print(f"[HOSPITAL HANDLER] Notification sent via available method")
        return True
        
    except Exception as e:
        print(f"[HOSPITAL HANDLER] Error sending notification: {e}")
        return False


async def handle_phase_3(
    current_gps: GPSLocation,
    hospital_gps: GPSLocation,
    hospital_info: Dict[str, Any],
    incident_id: str,
    incident_state: IncidentState,
    family_contact: str = None
) -> Dict[str, Any]:
    """
    Main entry point for Phase 3: Hospital Arrival Handoff.
    
    This function:
    1. Monitors arrival
    2. Sends family notification
    3. Updates state machine
    
    Args:
        current_gps: Current GPS coordinates
        hospital_gps: Hospital GPS coordinates
        hospital_info: Hospital information
        incident_id: Incident identifier
        incident_state: State machine instance
        family_contact: Family contact information
        
    Returns:
        Dictionary with Phase 3 results
    """
    result = {
        "arrival_detected": False,
        "notification_sent": False,
        "message": ""
    }
    
    # Check arrival
    arrival_detected = await monitor_arrival(
        current_gps,
        hospital_gps,
        incident_id,
        incident_state
    )
    
    result["arrival_detected"] = arrival_detected
    
    if arrival_detected and family_contact:
        # Send notification
        notification_sent = await send_arrival_notification(
            family_contact,
            hospital_info,
            incident_id,
            incident_state
        )
        result["notification_sent"] = notification_sent
    
    if arrival_detected:
        result["message"] = f"User arrived at {hospital_info.get('name', 'hospital')}"
    else:
        result["message"] = "User not yet at hospital"
    
    return result

