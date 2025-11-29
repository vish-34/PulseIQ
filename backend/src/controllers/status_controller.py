"""
Status Controller - Get incident status and logs
"""

from typing import Dict, Any, Optional
from models.incident_model import get_incident
from agents.core.state_machine import IncidentState


async def get_incident_status(incident_id: str) -> Dict[str, Any]:
    """
    Get current status of an incident.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        Dictionary with incident status information
    """
    incident = get_incident(incident_id)
    
    if not incident:
        return {
            "incident_id": incident_id,
            "status": "not_found",
            "message": "Incident not found"
        }
    
    # Get state machine status if available
    state_info = incident.get("state_info", {})
    
    return {
        "incident_id": incident_id,
        "state": incident.get("state", "unknown"),
        "created_at": incident.get("created_at"),
        "status": state_info.get("status", "active"),
        "logs_count": len(incident.get("logs", [])),
        "has_payload": "payload" in incident
    }


async def get_incident_logs(incident_id: str, limit: Optional[int] = None) -> Dict[str, Any]:
    """
    Get logs for an incident.
    
    Args:
        incident_id: Incident identifier
        limit: Maximum number of logs to return
        
    Returns:
        Dictionary with logs
    """
    incident = get_incident(incident_id)
    
    if not incident:
        return {
            "incident_id": incident_id,
            "logs": [],
            "message": "Incident not found"
        }
    
    logs = incident.get("logs", [])
    
    if limit:
        logs = logs[-limit:]
    
    return {
        "incident_id": incident_id,
        "logs": logs,
        "total_count": len(incident.get("logs", []))
    }

