"""
Agent Routes - API endpoints for incident status and management
"""

from fastapi import APIRouter, HTTPException
from typing import Optional
from controllers.status_controller import get_incident_status, get_incident_logs

router = APIRouter()


@router.get("/incident/{incident_id}/status")
async def get_status(incident_id: str):
    """
    Get current status of an incident.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        Incident status information
    """
    try:
        status = await get_incident_status(incident_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting status: {str(e)}")


@router.get("/incident/{incident_id}/logs")
async def get_logs(incident_id: str, limit: Optional[int] = None):
    """
    Get logs for an incident.
    
    Args:
        incident_id: Incident identifier
        limit: Maximum number of logs to return (optional)
        
    Returns:
        Incident logs
    """
    try:
        logs = await get_incident_logs(incident_id, limit)
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting logs: {str(e)}")


@router.post("/incident/{incident_id}/cancel")
async def cancel_incident(incident_id: str, reason: Optional[str] = None):
    """
    Cancel an incident (user responded or false alarm).
    
    Args:
        incident_id: Incident identifier
        reason: Cancellation reason (optional)
        
    Returns:
        Cancellation confirmation
    """
    try:
        from models.incident_model import get_incident, set_state
        
        incident = get_incident(incident_id)
        if not incident:
            raise HTTPException(status_code=404, detail="Incident not found")
        
        set_state(incident_id, "idle")
        
        return {
            "incident_id": incident_id,
            "status": "cancelled",
            "reason": reason or "User cancelled",
            "message": "Incident cancelled successfully"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error cancelling incident: {str(e)}")

