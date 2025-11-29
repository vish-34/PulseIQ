"""
Main FastAPI Application - Trauma Detection System

Entry point for the emergency response system.
"""

import asyncio
import sys
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from routes.trigger_routes import router as trigger_router
from routes.agent_routes import router as agent_router
from routes.twilio_routes import router as twilio_router
from routes.test_routes import router as test_router
from config.settings import settings
from utils.logger import logger
import time

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Multi-phase emergency response system for trauma detection",
    version="1.0.0"
)

# CORS middleware - Allow ALL requests (no blocking)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow ALL origins - no blocking
    allow_credentials=False,  # Set to False when using "*" for origins
    allow_methods=["*"],  # Allow ALL HTTP methods
    allow_headers=["*"],  # Allow ALL headers
    expose_headers=["*"],  # Expose ALL headers
    max_age=3600,  # Cache preflight for 1 hour
)


# Request logging middleware - Log ALL incoming requests
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all incoming requests to help debug connection issues"""
    start_time = time.time()
    
    # Get client info
    client_ip = request.client.host if request.client else "unknown"
    method = request.method
    url = str(request.url)
    path = request.url.path
    headers = dict(request.headers)
    
    # Log the request (but skip OPTIONS to reduce noise)
    if method != "OPTIONS":
        print("\n" + "="*70)
        print(f"🔔 INCOMING REQUEST DETECTED!")
        print("="*70)
        print(f"Method: {method}")
        print(f"Path: {path}")
        print(f"Full URL: {url}")
        print(f"Client IP: {client_ip}")
        print(f"Headers: {headers.get('user-agent', 'N/A')[:50]}")
        print(f"X-Trigger-Token: {headers.get('x-trigger-token', 'NOT PROVIDED')}")
        print(f"All Headers: {list(headers.keys())}")
        print("="*70 + "\n")
    elif method == "OPTIONS":
        # Just log OPTIONS briefly
        print(f"✓ OPTIONS preflight for {path} - Allowed")
    
    # Process request
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        print(f"✅ Request processed in {process_time:.2f}s - Status: {response.status_code}\n")
        return response
    except Exception as e:
        process_time = time.time() - start_time
        print(f"❌ Request failed after {process_time:.2f}s - Error: {e}\n")
        raise

# Include routers
app.include_router(trigger_router, prefix="/api/trigger", tags=["Trigger"])
app.include_router(agent_router, prefix="/api", tags=["Incidents"])
app.include_router(twilio_router, tags=["Twilio"])
app.include_router(test_router, prefix="/api", tags=["Test"])


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "operational",
        "service": settings.APP_NAME,
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": "1.0.0",
        "components": {
            "api": "operational",
            "state_machine": "operational",
            "agents": "operational"
        }
    }


@app.on_event("startup")
async def startup_event():
    """Run on server startup - Server waits for frontend button click"""
    print("\n" + "="*70)
    print("Trauma Detection System Started")
    print("="*70)
    print(f"Server running at: http://0.0.0.0:5000")
    print(f"API Docs at: http://0.0.0.0:5000/docs")
    print("\n" + "="*70)
    print("WAITING FOR FRONTEND BUTTON CLICK...")
    print("="*70)
    print("  - Frontend button: GET /api/trigger/crash")
    print("  - Custom payload: POST /api/trigger/crash")
    print("\nServer is ready. Crash simulation will ONLY start when button is clicked.")
    print("="*70 + "\n")


if __name__ == "__main__":
    import uvicorn
    
    # Server starts and waits for requests
    # NO AUTO-TEST - Only triggers when frontend button is clicked
    # Frontend can trigger via: GET /api/trigger/crash
    uvicorn.run(app, host="0.0.0.0", port=5000)

