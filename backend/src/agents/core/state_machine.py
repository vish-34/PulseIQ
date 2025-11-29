"""
Trauma Agent State Machine

This module implements a robust state machine for the trauma detection system.
It manages the lifecycle of an incident from detection to resolution.

State Flow:
1. idle -> triage (impact detected)
2. triage -> cancel_window (consciousness test initiated)
3. cancel_window -> confirmed (no voice detected) OR -> idle (voice detected)
4. confirmed -> dispatching (multi-agent swarm activated)
5. dispatching -> hospital_mode (arrived at hospital)
6. hospital_mode -> closed (incident resolved)
"""

from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum
from schemas.crash_payload import CrashPayloadInput, GPSLocation
from utils.logger import logger


class IncidentStateEnum(str, Enum):
    """Enumeration of all possible incident states - matches exact scenario"""
    IDLE = 'Idle'
    MONITORING = 'Monitoring'
    TRIANGULATION_PENDING = 'TriangulationPending'
    CRITICAL_CONFIRMED = 'CriticalConfirmed'
    AGENTS_RUNNING = 'AgentsRunning'
    HOSPITAL_MODE = 'HospitalMode'
    COMPLETED = 'Completed'


# Valid state transitions - matches exact scenario flow
VALID_TRANSITIONS: Dict[str, List[str]] = {
    'Idle': ['Monitoring'],
    'Monitoring': ['TriangulationPending', 'Idle'],
    'TriangulationPending': ['CriticalConfirmed', 'Idle'],
    'CriticalConfirmed': ['AgentsRunning'],
    'AgentsRunning': ['HospitalMode', 'Completed'],
    'HospitalMode': ['Completed'],
    'Completed': []  # Terminal state
}


class IncidentState:
    """
    State machine for managing trauma incident lifecycle.
    
    This class tracks the state of an incident and manages transitions
    between different phases of the emergency response protocol.
    """
    
    def __init__(self, incident_id: Optional[str] = None):
        """
        Initialize the state machine.
        
        Args:
            incident_id: Optional unique identifier for this incident
        """
        self.incident_id = incident_id
        self.state: str = IncidentStateEnum.IDLE.value
        logger.info("STATE_MACHINE", f"State machine initialized for incident: {incident_id or 'NEW'}")
        self.logs: List[Dict[str, Any]] = []
        self.payload: Optional[CrashPayloadInput] = None
        self.created_at: Optional[datetime] = None
        self.confirmed_at: Optional[datetime] = None
        self.hospital_gps: Optional[GPSLocation] = None
        self.metadata: Dict[str, Any] = {}
        
        self._log("State machine initialized", {"state": self.state})
    
    def _log(self, message: str, data: Optional[Dict[str, Any]] = None) -> None:
        """
        Internal logging method to track all state machine actions.
        
        Args:
            message: Log message
            data: Optional additional data to log
        """
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "state": self.state,
            "message": message,
            "data": data or {}
        }
        self.logs.append(log_entry)
    
    def can_transition(self, target_state: str) -> bool:
        """
        Check if a transition to the target state is valid.
        
        Args:
            target_state: The state to transition to
            
        Returns:
            True if transition is valid, False otherwise
        """
        if target_state not in IncidentStateEnum.__members__.values():
            return False
        
        valid_targets = VALID_TRANSITIONS.get(self.state, [])
        return target_state in valid_targets
    
    def transition(self, new_state: str, reason: str = "", data: Optional[Dict[str, Any]] = None) -> bool:
        """
        Attempt to transition to a new state.
        
        Args:
            new_state: The target state
            reason: Reason for the transition
            data: Optional additional data
            
        Returns:
            True if transition succeeded, False otherwise
        """
        if not self.can_transition(new_state):
            self._log(
                f"Invalid transition attempt: {self.state} -> {new_state}",
                {"reason": reason, "data": data}
            )
            return False
        
        old_state = self.state
        self.state = new_state
        
        self._log(
            f"State transition: {old_state} -> {new_state}",
            {"reason": reason, "data": data or {}}
        )
        
        return True
    
    def set_payload(self, payload: CrashPayloadInput) -> None:
        """
        Store the crash payload data.
        
        Args:
            payload: The crash payload input
        """
        self.payload = payload
        if not self.created_at:
            self.created_at = datetime.utcnow()
        self._log("Payload received and stored", {"gps": {"lat": payload.gps.lat, "lon": payload.gps.lon}})
    
    def start_monitoring(self, payload: CrashPayloadInput) -> bool:
        """
        Start monitoring phase when impact is detected.
        
        Transitions: Idle -> Monitoring
        
        Args:
            payload: The crash payload input
            
        Returns:
            True if transition succeeded
        """
        if self.transition(IncidentStateEnum.MONITORING.value, "Impact detected, starting monitoring"):
            self.set_payload(payload)
            logger.info("STATE_MACHINE", f"Transitioned to Monitoring - Impact detected at {payload.gps.lat}, {payload.gps.lon}")
            return True
        return False
    
    def start_triage(self, payload: CrashPayloadInput) -> bool:
        """
        Alias for start_monitoring (backward compatibility).
        
        Transitions: Idle -> Monitoring
        
        Args:
            payload: The crash payload input
            
        Returns:
            True if transition succeeded
        """
        return self.start_monitoring(payload)
    
    def start_triangulation(self) -> bool:
        """
        Start triangulation phase (consciousness test).
        
        The phone shouts "Impact detected. Speak to cancel." and listens for 5 seconds.
        
        Transitions: Monitoring -> TriangulationPending
        
        Returns:
            True if transition succeeded
        """
        if self.transition(
            IncidentStateEnum.TRIANGULATION_PENDING.value,
            "Triangulation initiated - consciousness test (5 seconds)"
        ):
            logger.info("STATE_MACHINE", "Triangulation pending - Consciousness test: 'Impact detected. Speak to cancel.'")
            return True
        return False
    
    def start_cancel_window(self) -> bool:
        """
        Alias for start_triangulation (backward compatibility).
        
        Transitions: Monitoring -> TriangulationPending
        
        Returns:
            True if transition succeeded
        """
        return self.start_triangulation()
    
    def confirm_critical_event(self) -> bool:
        """
        Confirm critical event after no voice response.
        
        This is Phase 1 completion - all 3 confirmations met.
        
        Transitions: TriangulationPending -> CriticalConfirmed
        
        Returns:
            True if transition succeeded
        """
        if self.transition(
            IncidentStateEnum.CRITICAL_CONFIRMED.value,
            "CRITICAL_EVENT_CONFIRMED - All 3 confirmations met (G-Force, Heart Rate, Silence)"
        ):
            self.confirmed_at = datetime.utcnow()
            logger.critical("STATE_MACHINE", "CRITICAL EVENT CONFIRMED - All 3 confirmations met")
            return True
        return False
    
    def cancel_incident(self, reason: str = "User responded during cancel window") -> bool:
        """
        Cancel the incident (user responded or false alarm).
        
        Transitions: TriangulationPending -> Idle OR Monitoring -> Idle
        
        Returns:
            True if transition succeeded
        """
        if self.state == IncidentStateEnum.TRIANGULATION_PENDING.value:
            logger.info("STATE_MACHINE", f"Incident cancelled: {reason}")
            return self.transition(IncidentStateEnum.IDLE.value, reason)
        elif self.state == IncidentStateEnum.MONITORING.value:
            logger.info("STATE_MACHINE", f"Incident cancelled: {reason}")
            return self.transition(IncidentStateEnum.IDLE.value, reason)
        return False
    
    def activate_protocol(self) -> bool:
        """
        Activate the multi-agent swarm protocol (Phase 2).
        
        This wakes up 3 sub-agents:
        - Agent A: The Dispatcher (Logistics)
        - Agent B: The Guardian (Medical Data)
        - Agent C: The Treasurer (Financial)
        
        Transitions: CriticalConfirmed -> AgentsRunning
        
        Returns:
            True if transition succeeded
        """
        if self.transition(
            IncidentStateEnum.AGENTS_RUNNING.value,
            "Multi-Agent Swarm activated - Agents A, B, C dispatched in parallel"
        ):
            logger.critical("STATE_MACHINE", "PHASE 2 ACTIVATED - Multi-Agent Swarm (Agents A, B, C)")
            return True
        return False
    
    def enter_hospital_mode(self, hospital_gps: GPSLocation) -> bool:
        """
        Enter hospital mode when user arrives at hospital (Phase 3).
        
        When phone GPS matches Hospital GPS, switch to Hospital Mode.
        Stops Black Box mode and notifies family.
        
        Transitions: AgentsRunning -> HospitalMode
        
        Args:
            hospital_gps: GPS coordinates of the hospital
            
        Returns:
            True if transition succeeded
        """
        if self.transition(
            IncidentStateEnum.HOSPITAL_MODE.value,
            "PHASE 3: User arrived at hospital - GPS geofence match confirmed",
            {"hospital_gps": {"lat": hospital_gps.lat, "lon": hospital_gps.lon}}
        ):
            self.hospital_gps = hospital_gps
            logger.success("STATE_MACHINE", f"Hospital Mode activated - GPS match at {hospital_gps.lat}, {hospital_gps.lon}")
            return True
        return False
    
    def close_incident(self, reason: str = "Incident resolved") -> bool:
        """
        Close the incident (mark as Completed).
        
        Transitions: HospitalMode -> Completed OR AgentsRunning -> Completed
        
        Args:
            reason: Reason for closing the incident
            
        Returns:
            True if transition succeeded
        """
        if self.transition(IncidentStateEnum.COMPLETED.value, reason):
            logger.success("STATE_MACHINE", f"Incident completed: {reason}")
            return True
        return False
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current status of the incident.
        
        Returns:
            Dictionary containing current state and relevant information
        """
        status = {
            "incident_id": self.incident_id,
            "state": self.state,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "log_count": len(self.logs),
            "has_payload": self.payload is not None
        }
        
        if self.payload:
            status["gps"] = {"lat": self.payload.gps.lat, "lon": self.payload.gps.lon}
            status["blood_type"] = self.payload.blood_type
        
        if self.hospital_gps:
            status["hospital_gps"] = {"lat": self.hospital_gps.lat, "lon": self.hospital_gps.lon}
        
        return status
    
    def get_recent_logs(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get the most recent log entries.
        
        Args:
            limit: Maximum number of logs to return
            
        Returns:
            List of recent log entries
        """
        return self.logs[-limit:] if self.logs else []
    
    def get_all_logs(self) -> List[Dict[str, Any]]:
        """
        Get all log entries.
        
        Returns:
            List of all log entries
        """
        return self.logs.copy()
    
    def update_metadata(self, key: str, value: Any) -> None:
        """
        Update incident metadata.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
        self._log(f"Metadata updated: {key}", {"key": key, "value": value})
    
    def is_terminal(self) -> bool:
        """
        Check if the state machine is in a terminal state.
        
        Returns:
            True if in terminal state (Completed), False otherwise
        """
        return self.state == IncidentStateEnum.COMPLETED.value
    
    def is_active(self) -> bool:
        """
        Check if the incident is currently active (not Idle or Completed).
        
        Returns:
            True if incident is active, False otherwise
        """
        return self.state not in [IncidentStateEnum.IDLE.value, IncidentStateEnum.COMPLETED.value]


# Convenience function to create a new incident state machine
def create_incident_state(incident_id: Optional[str] = None) -> IncidentState:
    """
    Factory function to create a new incident state machine.
    
    Args:
        incident_id: Optional unique identifier for the incident
        
    Returns:
        New IncidentState instance
    """
    return IncidentState(incident_id=incident_id)
