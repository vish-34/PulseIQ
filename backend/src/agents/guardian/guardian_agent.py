"""
Agent B: The Guardian (Medical Data)

Handles medical information display, QR code generation, and black box recording.
"""

from typing import Dict, Any
from schemas.crash_payload import CrashPayloadInput
from utils.qr_generator import generate_medical_qr, generate_first_responder_dashboard_data
from utils.black_box import start_black_box_recording
from utils.logger import logger


async def run(payload: CrashPayloadInput, incident_id: str) -> Dict[str, Any]:
    """
    Main execution function for Guardian Agent.
    
    Responsibilities:
    1. Override lock screen (force screen ON)
    2. Generate First Responder Dashboard
    3. Generate QR Code with medical info
    4. Start black box recording
    
    Args:
        payload: Crash payload input
        incident_id: Incident identifier
        
    Returns:
        Dictionary with results:
        {
            "success": bool,
            "lock_screen_overridden": bool,
            "qr_code_generated": bool,
            "dashboard_html": str,
            "recording_started": bool,
            "message": str
        }
    """
    result = {
        "success": False,
        "lock_screen_overridden": False,
        "qr_code_generated": False,
        "dashboard_html": "",
        "recording_started": False,
        "message": ""
    }
    
    try:
        # Step 1: Override lock screen (force screen ON)
        logger.info("GUARDIAN", "Overriding lock screen - Force screen ON")
        result["lock_screen_overridden"] = override_lock_screen()
        logger.success("GUARDIAN", f"Lock screen override: {result['lock_screen_overridden']}")
        
        # Step 2: Prepare medical data
        medical_data = {
            "blood_type": payload.blood_type,
            "allergies": payload.allergies,
            "emergency_contact": "Emergency Contact",  # Would come from user profile
            "incident_id": incident_id,
            "vitals": {
                "heart_rate": payload.heart_rate,
                "heart_rate_after": payload.heart_rate_after,
                "g_force": payload.g_force
            }
        }
        
        # Step 3: Generate First Responder Dashboard
        logger.info("GUARDIAN", "Generating First Responder Dashboard")
        dashboard_html = generate_first_responder_dashboard_data(medical_data)
        result["dashboard_html"] = dashboard_html
        logger.success("GUARDIAN", "First Responder Dashboard generated - Displaying: Blood type, Allergies, Medications, QR")
        
        # Step 4: Generate QR Code
        logger.info("GUARDIAN", "Generating medical QR code with user ID and vitals")
        qr_code_bytes = generate_medical_qr(medical_data)
        result["qr_code_generated"] = True
        result["qr_code_bytes"] = qr_code_bytes
        logger.success("GUARDIAN", f"QR code generated ({len(qr_code_bytes)} bytes)")
        
        # Step 5: Start black box recording (rolling 60-second buffer)
        logger.info("GUARDIAN", "Starting Black Box Mode - Continuous audio recording")
        recorder = start_black_box_recording(incident_id)
        result["recording_started"] = True
        result["recording_id"] = recorder.recording_id
        logger.success("GUARDIAN", f"Black Box recording started: {recorder.recording_id} - Rolling 60s buffer active")
        
        result["success"] = True
        result["message"] = "Guardian agent completed all tasks"
        logger.success("GUARDIAN", "All tasks completed: Lock override, Dashboard, QR, Black Box")
        
    except Exception as e:
        result["message"] = f"Guardian agent error: {str(e)}"
        logger.error("GUARDIAN", f"Error: {e}")
    
    return result


def override_lock_screen() -> bool:
    """
    Override the lock screen to keep phone screen ON.
    
    In a real mobile app, this would:
    - Request WAKE_LOCK permission
    - Keep screen on programmatically
    - Display emergency dashboard
    
    For backend demo, we simulate this.
    
    Returns:
        True if successful
    """
    # In production, this would interact with mobile OS
    # For backend demo, we just return success
    return True



