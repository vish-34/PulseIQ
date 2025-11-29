"""
Family Notification Utilities

Handles all family notifications (email, call, SMS) for crash alerts and hospital arrival.
"""

from typing import Dict, Any
from config.settings import settings
from utils.logger import logger
from agents.tools.email_service import send_family_notification
from agents.tools.twilio_service import make_call, send_sms


async def notify_family_crash_alert(
    incident_id: str,
    gps_lat: float,
    gps_lon: float,
    blood_type: str
) -> Dict[str, Any]:
    """
    Notify family when crash is confirmed (Phase 1 completion).
    
    Sends:
    - Email to FAMILY_EMAIL
    - Phone call to FAMILY_PHONE
    - SMS to FAMILY_PHONE
    
    Args:
        incident_id: Incident identifier
        gps_lat: GPS latitude
        gps_lon: GPS longitude
        blood_type: Patient blood type
        
    Returns:
        Dictionary with notification results
    """
    result = {
        "email_sent": False,
        "call_made": False,
        "sms_sent": False,
        "success": False
    }
    
    logger.info("FAMILY_NOTIFY", "Sending crash alert to family (email + call + SMS)")
    
    # Prepare crash alert message (enhanced)
    crash_message = (
        f"Emergency Alert. Your family member has undergone a severe accidental crash. "
        f"Emergency services have been alerted and are on the way to the location. "
        f"GPS coordinates: {gps_lat}, {gps_lon}. "
        f"Incident reference number: {incident_id}. "
        f"Patient blood type: {blood_type}. "
        f"Please stay available for further updates. Help is on the way."
    )
    
    # Prepare email content
    incident_info = {
        "incident_id": incident_id,
        "hospital_name": "Emergency Services Dispatched",
        "hospital_address": f"Lat: {gps_lat}, Lon: {gps_lon}",
        "status": "crash_detected_emergency_dispatched",
        "message": crash_message
    }
    
    # 1. Send Email
    if settings.FAMILY_EMAIL:
        try:
            logger.info("FAMILY_NOTIFY", f"Sending crash alert email to {settings.FAMILY_EMAIL}")
            email_sent = await send_family_notification(
                family_email=settings.FAMILY_EMAIL,
                incident_info=incident_info
            )
            result["email_sent"] = email_sent
            if email_sent:
                logger.success("FAMILY_NOTIFY", f"Crash alert email sent to {settings.FAMILY_EMAIL}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to send crash alert email to {settings.FAMILY_EMAIL}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error sending crash alert email: {e}")
    
    # 2. Make Phone Call
    if settings.FAMILY_PHONE:
        try:
            logger.info("FAMILY_NOTIFY", f"Making crash alert call to {settings.FAMILY_PHONE}")
            call_result = await make_call(settings.FAMILY_PHONE, crash_message)
            if call_result.get("call_id") or call_result.get("success"):
                result["call_made"] = True
                logger.success("FAMILY_NOTIFY", f"Crash alert call made to {settings.FAMILY_PHONE} - Call ID: {call_result.get('call_id', 'N/A')}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to make crash alert call to {settings.FAMILY_PHONE} - Result: {call_result}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error making crash alert call: {e}")
            import traceback
            logger.error("FAMILY_NOTIFY", f"Traceback: {traceback.format_exc()}")
    
    # 3. Send SMS
    if settings.FAMILY_PHONE:
        try:
            sms_message = (
                f"Emergency Alert. Crash detected at {gps_lat}, {gps_lon}. "
                f"Emergency services dispatched. Incident ID: {incident_id}."
            )
            logger.info("FAMILY_NOTIFY", f"Sending crash alert SMS to {settings.FAMILY_PHONE}")
            sms_result = await send_sms(settings.FAMILY_PHONE, sms_message)
            if sms_result.get("success") or sms_result.get("message_id"):
                result["sms_sent"] = True
                logger.success("FAMILY_NOTIFY", f"Crash alert SMS sent to {settings.FAMILY_PHONE} - Message ID: {sms_result.get('message_id', 'N/A')}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to send crash alert SMS to {settings.FAMILY_PHONE}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error sending crash alert SMS: {e}")
    
    result["success"] = result["email_sent"] or result["call_made"] or result["sms_sent"]
    
    if result["success"]:
        logger.success("FAMILY_NOTIFY", "✅ Family crash alert notifications sent (email, call, SMS)")
    else:
        logger.warn("FAMILY_NOTIFY", "⚠️ No family notifications sent - check FAMILY_EMAIL and FAMILY_PHONE in settings")
    
    return result


async def notify_family_hospital_arrival(
    incident_id: str,
    hospital_name: str,
    hospital_gps_lat: float,
    hospital_gps_lon: float
) -> Dict[str, Any]:
    """
    Notify family when user arrives at hospital (Phase 3).
    
    Sends:
    - Email to FAMILY_EMAIL
    - Phone call to FAMILY_PHONE
    - SMS to FAMILY_PHONE
    
    Args:
        incident_id: Incident identifier
        hospital_name: Hospital name
        hospital_gps_lat: Hospital GPS latitude
        hospital_gps_lon: Hospital GPS longitude
        
    Returns:
        Dictionary with notification results
    """
    result = {
        "email_sent": False,
        "call_made": False,
        "sms_sent": False,
        "success": False
    }
    
    logger.info("FAMILY_NOTIFY", "Sending hospital arrival update to family (email + call + SMS)")
    
    # Prepare hospital arrival message (enhanced)
    arrival_message = (
        f"Update: Your family member has arrived at the hospital and is now being admitted. "
        f"Hospital name: {hospital_name}. "
        f"Please check your email for hospital admission fees and detailed information. "
        f"Incident reference number: {incident_id}. "
        f"Medical team is providing care. We will keep you updated."
    )
    
    # Prepare email content
    incident_info = {
        "incident_id": incident_id,
        "hospital_name": hospital_name,
        "hospital_address": f"Lat: {hospital_gps_lat}, Lon: {hospital_gps_lon}",
        "status": "stabilization_in_progress",
        "message": arrival_message
    }
    
    # 1. Send Email
    if settings.FAMILY_EMAIL:
        try:
            logger.info("FAMILY_NOTIFY", f"Sending hospital arrival email to {settings.FAMILY_EMAIL}")
            email_sent = await send_family_notification(
                family_email=settings.FAMILY_EMAIL,
                incident_info=incident_info
            )
            result["email_sent"] = email_sent
            if email_sent:
                logger.success("FAMILY_NOTIFY", f"Hospital arrival email sent to {settings.FAMILY_EMAIL}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to send hospital arrival email to {settings.FAMILY_EMAIL}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error sending hospital arrival email: {e}")
    
    # 2. Make Phone Call
    if settings.FAMILY_PHONE:
        try:
            logger.info("FAMILY_NOTIFY", f"Making hospital arrival call to {settings.FAMILY_PHONE}")
            call_result = await make_call(settings.FAMILY_PHONE, arrival_message)
            if call_result.get("call_id") or call_result.get("success"):
                result["call_made"] = True
                logger.success("FAMILY_NOTIFY", f"Hospital arrival call made to {settings.FAMILY_PHONE} - Call ID: {call_result.get('call_id', 'N/A')}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to make hospital arrival call to {settings.FAMILY_PHONE} - Result: {call_result}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error making hospital arrival call: {e}")
            import traceback
            logger.error("FAMILY_NOTIFY", f"Traceback: {traceback.format_exc()}")
    
    # 3. Send SMS
    if settings.FAMILY_PHONE:
        try:
            sms_message = f"Update: User has reached {hospital_name}. Stabilization in progress. Incident ID: {incident_id}."
            logger.info("FAMILY_NOTIFY", f"Sending hospital arrival SMS to {settings.FAMILY_PHONE}")
            sms_result = await send_sms(settings.FAMILY_PHONE, sms_message)
            if sms_result.get("success") or sms_result.get("message_id"):
                result["sms_sent"] = True
                logger.success("FAMILY_NOTIFY", f"Hospital arrival SMS sent to {settings.FAMILY_PHONE} - Message ID: {sms_result.get('message_id', 'N/A')}")
            else:
                logger.warn("FAMILY_NOTIFY", f"Failed to send hospital arrival SMS to {settings.FAMILY_PHONE}")
        except Exception as e:
            logger.error("FAMILY_NOTIFY", f"Error sending hospital arrival SMS: {e}")
    
    result["success"] = result["email_sent"] or result["call_made"] or result["sms_sent"]
    
    if result["success"]:
        logger.success("FAMILY_NOTIFY", "✅ Family hospital arrival notifications sent (email, call, SMS)")
    else:
        logger.warn("FAMILY_NOTIFY", "⚠️ No family notifications sent - check FAMILY_EMAIL and FAMILY_PHONE in settings")
    
    return result

