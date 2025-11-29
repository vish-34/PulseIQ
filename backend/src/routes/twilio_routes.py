"""
Twilio Webhook Routes

Handles Twilio callbacks and TwiML responses for phone calls.
"""

from fastapi import APIRouter, Request, Query
from fastapi.responses import Response
from typing import Optional
import urllib.parse

router = APIRouter()


@router.post("/twilio/voice")
async def twilio_voice_webhook(request: Request):
    """
    Twilio webhook endpoint for voice calls.
    Returns TwiML that plays the message automatically.
    
    This endpoint is called by Twilio when a call is answered.
    The message is passed as a query parameter.
    """
    # Get message from query parameters
    form_data = await request.form()
    message = form_data.get("Message", "")
    
    # If message is in query params instead
    if not message:
        query_params = dict(request.query_params)
        message = query_params.get("message", "")
    
    # Decode URL-encoded message
    if message:
        message = urllib.parse.unquote(message)
    
    # If no message provided, use default
    if not message:
        message = "Emergency alert. Please check your email for details."
    
    # Escape XML special characters
    escaped_message = (
        message
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    
    # Generate TwiML response - plays message IMMEDIATELY
    # No <Gather> - just direct <Say> so it plays right away
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{escaped_message}</Say>
    <Hangup/>
</Response>'''
    
    return Response(content=twiml, media_type="application/xml")


@router.get("/twilio/voice")
async def twilio_voice_webhook_get(message: Optional[str] = Query(None)):
    """
    Twilio webhook endpoint (GET method) for voice calls.
    Returns TwiML that plays the message automatically.
    """
    # If no message provided, use default
    if not message:
        message = "Emergency alert. Please check your email for details."
    
    # Decode URL-encoded message
    message = urllib.parse.unquote(message)
    
    # Escape XML special characters
    escaped_message = (
        message
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;")
    )
    
    # Generate TwiML response - plays message IMMEDIATELY
    # No <Gather> - just direct <Say> so it plays right away
    twiml = f'''<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice">{escaped_message}</Say>
    <Hangup/>
</Response>'''
    
    return Response(content=twiml, media_type="application/xml")

