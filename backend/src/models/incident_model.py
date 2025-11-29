"""
Incident Model - In-memory incident storage

In production, this would use a database.
"""

from typing import Dict, Any, Optional
from datetime import datetime

# In-memory storage
INCIDENTS: Dict[str, Dict[str, Any]] = {}


def new_incident(payload: Dict[str, Any]) -> Dict[str, Any]:
    """
    Create a new incident record.
    
    Args:
        payload: Incident data dictionary
        
    Returns:
        Created incident dictionary
    """
    incident_id = payload.get("incident_id", f"inc_{int(datetime.utcnow().timestamp())}")
    
    incident = {
        "incident_id": incident_id,
        "created_at": payload.get("created_at", datetime.utcnow().isoformat()),
        "state": payload.get("state", "triage"),
        "payload": payload.get("payload", {}),
        "logs": [],
        "tasks": {},
        "metadata": {}
    }
    
    INCIDENTS[incident_id] = incident
    return incident


def get_incident(incident_id: str) -> Optional[Dict[str, Any]]:
    """
    Get incident by ID.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        Incident dictionary or None if not found
    """
    return INCIDENTS.get(incident_id)


def add_log(incident_id: str, message: str) -> None:
    """
    Add a log entry to an incident.
    
    Args:
        incident_id: Incident identifier
        message: Log message
    """
    inc = INCIDENTS.get(incident_id)
    if not inc:
        return
    
    ts = datetime.utcnow().isoformat()
    log_entry = f"{ts} | {message}"
    inc["logs"].append(log_entry)


def set_state(incident_id: str, state: str) -> None:
    """
    Update incident state.
    
    Args:
        incident_id: Incident identifier
        state: New state
    """
    inc = INCIDENTS.get(incident_id)
    if not inc:
        return
    inc["state"] = state


def update_incident(incident_id: str, updates: Dict[str, Any]) -> bool:
    """
    Update incident with new data.
    
    Args:
        incident_id: Incident identifier
        updates: Dictionary of updates
        
    Returns:
        True if updated, False if incident not found
    """
    inc = INCIDENTS.get(incident_id)
    if not inc:
        return False
    
    inc.update(updates)
    return True
