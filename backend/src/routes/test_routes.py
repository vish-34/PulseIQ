"""
Test Routes - Diagnostic endpoints to verify connection
"""

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from utils.logger import logger
from datetime import datetime

router = APIRouter()


@router.get("/test")
async def test_endpoint(request: Request):
    """
    Simple test endpoint to verify backend is reachable.
    No authentication required - just returns success.
    """
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    
    logger.info("TEST", f"Test endpoint called from: {client_ip}")
    logger.info("TEST", f"User-Agent: {user_agent[:100]}")
    
    return JSONResponse({
        "status": "success",
        "message": "Backend is reachable!",
        "timestamp": datetime.utcnow().isoformat(),
        "client_ip": client_ip,
        "user_agent": user_agent
    })


@router.get("/test/crash-endpoint")
async def test_crash_endpoint(request: Request):
    """
    Test endpoint that simulates the crash endpoint (without triggering crash).
    Checks if headers are being sent correctly.
    """
    client_ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent", "unknown")
    trigger_token = request.headers.get("x-trigger-token", "NOT PROVIDED")
    
    logger.info("TEST", f"Crash endpoint test called from: {client_ip}")
    logger.info("TEST", f"X-Trigger-Token header: {trigger_token}")
    logger.info("TEST", f"User-Agent: {user_agent[:100]}")
    
    has_token = trigger_token == "CRASH_BUTTON"
    
    return JSONResponse({
        "status": "success",
        "message": "Crash endpoint test - connection working!",
        "timestamp": datetime.utcnow().isoformat(),
        "client_ip": client_ip,
        "headers_received": {
            "x-trigger-token": trigger_token,
            "has_valid_token": has_token,
            "user_agent": user_agent
        },
        "note": "This is just a test. Actual crash endpoint is /api/trigger/crash"
    })

