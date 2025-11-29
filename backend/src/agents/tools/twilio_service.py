"""
Twilio Service - Emergency Calls and SMS

Handles automated emergency calls with TTS and SMS notifications.
"""

import asyncio
import random
from typing import Dict, Any, Optional
from twilio.rest import Client
from twilio.twiml.voice_response import VoiceResponse
from config.settings import settings
from utils.logger import logger


async def make_call(phone_number: str, message: str) -> Dict[str, Any]:
    """
    Make a TTS (Text-to-Speech) call to the specified phone number.
    
    Args:
        phone_number: Phone number to call (E.164 format)
        message: Message to speak via TTS
        
    Returns:
        Dictionary with call information:
        {
            "call_id": str,
            "status": str,
            "transcript": str,
            "success": bool
        }
    """
    # Check if Twilio credentials are configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
        logger.warn("TWILIO", f"Twilio credentials not configured - using mock call to {phone_number}")
        return await _mock_make_call(phone_number, message)
    
    try:
        logger.info("TWILIO", f"Making real Twilio call to {phone_number}")
        logger.info("TWILIO", f"From: {settings.TWILIO_PHONE_NUMBER}")
        logger.info("TWILIO", f"Account SID: {settings.TWILIO_ACCOUNT_SID[:10]}...")
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        # Use TwiML that plays message IMMEDIATELY after trial verification
        # No <Gather> - just direct <Say> so it plays right away without any delay or keypress
        escaped_message = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace("'", "&apos;")
        
        # Simple TwiML structure - plays message immediately when TwiML executes
        # After trial verification completes (user presses key or it times out), this plays immediately
        twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{escaped_message}</Say>
    <Hangup/>
</Response>'''
        
        logger.info("TWILIO", "Using immediate-play TwiML - Message will play RIGHT AFTER trial verification")
        logger.info("TWILIO", "Note: Trial verification plays first (Twilio requirement), then your message plays IMMEDIATELY (no delay, no keypress needed)")
        logger.info("TWILIO", f"TwiML length: {len(twiml)} characters")
        
        # Create the call - this is the critical step
        logger.info("TWILIO", "Creating Twilio call...")
        call = client.calls.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            twiml=twiml
        )
        
        # Store call info before logging (to avoid encoding issues)
        call_sid = call.sid
        call_status = call.status
        
        # Log success (without emoji to avoid Windows encoding issues)
        logger.info("TWILIO", f"Call created successfully!")
        logger.info("TWILIO", f"Call SID: {call_sid}")
        logger.info("TWILIO", f"Call status: {call_status}")
        
        # Return immediately - call is created
        return {
            "call_id": call_sid,
            "status": call_status,
            "transcript": f"Call placed to {phone_number}: {message}",
            "success": True
        }
    except Exception as e:
        logger.error("TWILIO", f"Twilio call error: {e}")
        logger.error("TWILIO", f"Error type: {type(e).__name__}")
        import traceback
        logger.error("TWILIO", f"Traceback: {traceback.format_exc()}")
        # Fallback to mock
        logger.warn("TWILIO", f"Falling back to mock call for {phone_number}")
        return await _mock_make_call(phone_number, message)


async def send_sms(phone_number: str, message: str) -> Dict[str, Any]:
    """
    Send SMS to the specified phone number.
    
    Args:
        phone_number: Phone number to send SMS to (E.164 format)
        message: SMS message content
        
    Returns:
        Dictionary with SMS information:
        {
            "message_id": str,
            "status": str,
            "success": bool
        }
    """
    # Check if Twilio credentials are configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN or not settings.TWILIO_PHONE_NUMBER:
        logger.warn("TWILIO", f"Twilio credentials not configured - using mock SMS to {phone_number}")
        return await _mock_send_sms(phone_number, message)
    
    try:
        logger.info("TWILIO", f"Sending real Twilio SMS to {phone_number}")
        logger.info("TWILIO", f"From: {settings.TWILIO_PHONE_NUMBER}")
        
        client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
        
        message_obj = client.messages.create(
            to=phone_number,
            from_=settings.TWILIO_PHONE_NUMBER,
            body=message
        )
        
        logger.success("TWILIO", f"SMS sent successfully - Message SID: {message_obj.sid}")
        logger.info("TWILIO", f"Message status: {message_obj.status}")
        
        return {
            "message_id": message_obj.sid,
            "status": message_obj.status,
            "success": True
        }
    except Exception as e:
        logger.error("TWILIO", f"Twilio SMS error: {e}")
        logger.error("TWILIO", f"Error type: {type(e).__name__}")
        import traceback
        logger.error("TWILIO", f"Traceback: {traceback.format_exc()}")
        # Fallback to mock
        logger.warn("TWILIO", f"Falling back to mock SMS for {phone_number}")
        return await _mock_send_sms(phone_number, message)


async def make_emergency_call(
    dispatcher_number: str,
    alert_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Make a structured emergency call to dispatcher with formatted message.
    
    Args:
        dispatcher_number: Emergency dispatcher phone number
        alert_data: Dictionary containing:
            - location: {"lat": float, "lon": float}
            - blood_type: str
            - user_unresponsive: bool
            - incident_id: str
            
    Returns:
        Dictionary with call information
    """
    # Format the "Ghost Voice" message
    lat = alert_data.get("location", {}).get("lat", 0)
    lon = alert_data.get("location", {}).get("lon", 0)
    blood_type = alert_data.get("blood_type", "Unknown")
    incident_id = alert_data.get("incident_id", "Unknown")
    
    message = (
        f"Automated Alert. Severe Crash at coordinates {lat:.6f}, {lon:.6f}. "
        f"User Unresponsive. Blood Type {blood_type}. "
        f"Incident ID {incident_id}. Dispatch ACLS unit immediately."
    )
    
    return await make_call(dispatcher_number, message)


async def _mock_make_call(phone_number: str, message: str) -> Dict[str, Any]:
    """Mock call implementation for demo/testing"""
    await asyncio.sleep(0.2 + random.random() * 0.4)
    call_id = f"call_{random.getrandbits(32):08x}"
    transcript = f"Synthetic call to {phone_number} with message: {message}"
    
    # Print to console for visibility
    print("\n" + "="*70)
    print("📞 [MOCK CALL] Emergency Call Simulated")
    print("="*70)
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"Call ID: {call_id}")
    print("="*70 + "\n")
    print("⚠️  NOTE: This is a MOCK call. For real calls, add Twilio credentials to .env")
    print("="*70 + "\n")
    
    return {
        "call_id": call_id,
        "status": "dispatched",
        "transcript": transcript
    }


async def _mock_send_sms(phone_number: str, message: str) -> Dict[str, Any]:
    """Mock SMS implementation for demo/testing"""
    await asyncio.sleep(0.1 + random.random() * 0.2)
    message_id = f"sms_{random.getrandbits(32):08x}"
    
    # Print to console for visibility (no emoji to avoid Windows encoding issues)
    print("\n" + "="*70)
    print("[MOCK SMS] SMS Simulated")
    print("="*70)
    print(f"To: {phone_number}")
    print(f"Message: {message}")
    print(f"Message ID: {message_id}")
    print("="*70 + "\n")
    print("NOTE: This is a MOCK SMS. For real SMS, add Twilio credentials to .env")
    print("="*70 + "\n")
    
    return {
        "message_id": message_id,
        "status": "sent"
    }
