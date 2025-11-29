"""
Trigger Routes - API endpoints for crash detection
"""

from fastapi import APIRouter, HTTPException, Header, Request
from typing import Optional, Dict, Any
from schemas.crash_payload import CrashPayloadInput, CrashPayloadOutput, GPSLocation
from controllers.trigger_controller import handle_crash_trigger
from utils.logger import logger
from utils.crash_task_manager import cancel_crash_simulation, get_active_incident_ids, cancel_all_simulations
import asyncio

router = APIRouter()


@router.options("/crash")
async def trigger_crash_options():
    """
    Handle CORS preflight OPTIONS request.
    This allows the browser to check if the actual request is allowed.
    """
    from fastapi.responses import Response
    logger.info("API", "OPTIONS request received (CORS preflight) - Allowing")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "X-Trigger-Token, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
    )


@router.get("/crash", response_model=CrashPayloadOutput)
async def trigger_crash_get(
    request: Request,
    x_trigger_token: Optional[str] = Header(None, alias="X-Trigger-Token")
) -> CrashPayloadOutput:
    """
    Trigger crash detection via GET request (for frontend button).
    
    This endpoint is called when the frontend "Crash Button" is pressed.
    Uses default test data with NESCO Centre Goregaon location.
    
    SECURITY: Requires X-Trigger-Token header to prevent accidental triggers
    from link previews (WhatsApp, Telegram), bots, or direct browser access.
    
    Args:
        request: FastAPI request object (to check User-Agent)
        x_trigger_token: Required header token (must be "CRASH_BUTTON" from frontend)
    
    Returns:
        CrashPayloadOutput with incident details and response status
    """
    # Check User-Agent to identify link preview bots
    user_agent = request.headers.get("user-agent", "").lower()
    
    # List of known link preview bots and automated tools
    blocked_agents = [
        "whatsapp",
        "telegram",
        "facebookexternalhit",
        "twitterbot",
        "linkedinbot",
        "slackbot",
        "discordbot",
        "googlebot",
        "bingbot",
        "curl",
        "wget",
        "python-requests",
        "postman",
        "insomnia"
    ]
    
    is_blocked_agent = any(blocked in user_agent for blocked in blocked_agents)
    
    # REQUIRE the header token for all requests
    # This prevents accidental triggers from link previews
    if x_trigger_token != "CRASH_BUTTON":
        if is_blocked_agent:
            logger.warn("API", f"Blocked link preview/bot request: {user_agent[:50]}")
        else:
            logger.warn("API", "="*70)
            logger.warn("API", "GET /api/trigger/crash called without valid X-Trigger-Token header")
            logger.warn("API", f"Received token: '{x_trigger_token}' (expected: 'CRASH_BUTTON')")
            logger.warn("API", f"All headers: {dict(request.headers)}")
            logger.warn("API", "="*70)
        
        raise HTTPException(
            status_code=403,
            detail="This endpoint requires X-Trigger-Token: CRASH_BUTTON header. Use from frontend button only."
        )
    
    logger.info("API", "="*70)
    logger.info("API", "GET /api/trigger/crash - Crash button pressed from frontend (valid token)")
    logger.info("API", f"Request received from: {request.client.host if request.client else 'unknown'}")
    logger.info("API", "="*70)
    
    # Create default test payload - NESCO Centre Goregaon location
    default_payload = CrashPayloadInput(
        g_force=5.2,
        heart_rate=145.0,
        heart_rate_after=45.0,
        voice_decibels=0.0,
        gps=GPSLocation(lat=19.1680, lon=72.8500),  # NESCO Centre Goregaon East, Mumbai
        blood_type="O+",
        allergies=["Penicillin"],
        user_consent=True
    )
    
    logger.info("API", "Creating crash payload and starting simulation...")
    logger.info("API", f"Payload: G-Force={default_payload.g_force}, HR={default_payload.heart_rate}, HR_after={default_payload.heart_rate_after}, Voice={default_payload.voice_decibels}")
    
    try:
        logger.info("API", "="*70)
        logger.info("API", "CALLING handle_crash_trigger() NOW...")
        logger.info("API", "This will take ~35 seconds (5s consciousness test + 30s transport)")
        logger.info("API", "="*70)
        
        # Call the crash trigger - this should block until complete
        result = await handle_crash_trigger(default_payload)
        
        logger.success("API", "="*70)
        logger.success("API", "handle_crash_trigger() COMPLETED!")
        logger.success("API", "Crash simulation triggered successfully via GET request")
        logger.success("API", f"Incident ID: {result.incident_id}")
        logger.success("API", f"Status: {result.status}")
        logger.success("API", "="*70)
        return result
    except Exception as e:
        import traceback
        logger.error("API", "="*70)
        logger.error("API", f"ERROR processing crash trigger: {e}")
        logger.error("API", f"Traceback: {traceback.format_exc()}")
        logger.error("API", "="*70)
        raise HTTPException(status_code=500, detail=f"Error processing crash trigger: {str(e)}")


@router.post("/crash", response_model=CrashPayloadOutput)
async def trigger_crash_post(payload: CrashPayloadInput) -> CrashPayloadOutput:
    """
    Trigger crash detection and emergency response with custom payload.
    
    This is the main entry point for the trauma detection system.
    Receives sensor data and initiates the full emergency response protocol.
    
    Args:
        payload: Crash payload with sensor data
        
    Returns:
        CrashPayloadOutput with incident details and response status
    """
    logger.info("API", "POST /api/trigger/crash - Custom crash payload received")
    
    try:
        result = await handle_crash_trigger(payload)
        return result
    except Exception as e:
        logger.error("API", f"Error processing crash trigger: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing crash trigger: {str(e)}")
    except asyncio.CancelledError:
        logger.warn("API", "Crash simulation was cancelled by stop button")
        raise HTTPException(status_code=499, detail="Crash simulation cancelled by stop button")


@router.options("/cancel")
async def cancel_crash_options():
    """
    Handle CORS preflight OPTIONS request for cancel endpoint.
    """
    from fastapi.responses import Response
    logger.info("API", "OPTIONS request received for /cancel (CORS preflight) - Allowing")
    return Response(
        status_code=200,
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
            "Access-Control-Allow-Headers": "X-Trigger-Token, Content-Type",
            "Access-Control-Max-Age": "3600"
        }
    )


@router.get("/cancel")
async def cancel_crash_get(
    request: Request,
    x_trigger_token: Optional[str] = Header(None, alias="X-Trigger-Token")
) -> Dict[str, Any]:
    """
    Cancel ongoing crash simulation via GET request (for frontend stop button).
    
    This endpoint is called when the frontend "Stop Button" is pressed.
    It cancels the currently running crash simulation.
    
    SECURITY: Requires X-Trigger-Token header to prevent accidental cancellation.
    
    Args:
        request: FastAPI request object
        x_trigger_token: Required header token (must be "CRASH_BUTTON" from frontend)
    
    Returns:
        Dictionary with cancellation status
    """
    # Check token
    if x_trigger_token != "CRASH_BUTTON":
        logger.warn("API", "="*70)
        logger.warn("API", "GET /api/trigger/cancel called without valid X-Trigger-Token header")
        logger.warn("API", f"Received token: '{x_trigger_token}' (expected: 'CRASH_BUTTON')")
        logger.warn("API", "="*70)
        raise HTTPException(
            status_code=403,
            detail="This endpoint requires X-Trigger-Token: CRASH_BUTTON header."
        )
    
    logger.info("API", "="*70)
    logger.info("API", "GET /api/trigger/cancel - Stop button pressed from frontend")
    logger.info("API", f"Request received from: {request.client.host if request.client else 'unknown'}")
    logger.info("API", "="*70)
    
    # Get active incident IDs
    active_incidents = get_active_incident_ids()
    
    if not active_incidents:
        logger.warn("API", "No active crash simulations to cancel")
        return {
            "success": False,
            "message": "No active crash simulation found",
            "cancelled_count": 0
        }
    
    # Cancel all active simulations (usually just one)
    cancelled_count = cancel_all_simulations()
    
    logger.success("API", "="*70)
    logger.success("API", f"✅ Cancelled {cancelled_count} crash simulation(s)")
    logger.success("API", f"Active incidents cancelled: {active_incidents}")
    logger.success("API", "="*70)
    
    return {
        "success": True,
        "message": f"Cancelled {cancelled_count} crash simulation(s)",
        "cancelled_count": cancelled_count,
        "cancelled_incidents": active_incidents
    }

