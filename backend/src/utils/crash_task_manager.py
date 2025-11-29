"""
Crash Task Manager - Tracks and manages running crash simulations

Allows cancellation of ongoing crash simulations via stop button.
"""

from typing import Dict, Optional
import asyncio
from utils.logger import logger

# Global storage for active crash simulation tasks
# Key: incident_id, Value: asyncio.Task
_active_crash_tasks: Dict[str, asyncio.Task] = {}

# Global storage for cancellation flags
# Key: incident_id, Value: bool (True = cancelled)
_cancellation_flags: Dict[str, bool] = {}


def register_crash_task(incident_id: str, task: asyncio.Task) -> None:
    """
    Register a running crash simulation task.
    
    Args:
        incident_id: Incident identifier
        task: The asyncio task running the crash simulation
    """
    _active_crash_tasks[incident_id] = task
    _cancellation_flags[incident_id] = False
    logger.info("TASK_MANAGER", f"Registered crash task for incident: {incident_id}")


def cancel_crash_simulation(incident_id: str) -> bool:
    """
    Cancel a running crash simulation.
    
    Args:
        incident_id: Incident identifier to cancel
        
    Returns:
        True if cancellation was initiated, False if task not found
    """
    if incident_id in _cancellation_flags:
        _cancellation_flags[incident_id] = True
        logger.warn("TASK_MANAGER", f"Cancellation flag set for incident: {incident_id}")
        
        # Cancel the asyncio task if it exists
        if incident_id in _active_crash_tasks:
            task = _active_crash_tasks[incident_id]
            if not task.done():
                task.cancel()
                logger.warn("TASK_MANAGER", f"Cancelled asyncio task for incident: {incident_id}")
                return True
            else:
                logger.info("TASK_MANAGER", f"Task for incident {incident_id} already completed")
                return True
        return True
    else:
        logger.warn("TASK_MANAGER", f"No active task found for incident: {incident_id}")
        return False


def is_cancelled(incident_id: str) -> bool:
    """
    Check if a crash simulation has been cancelled.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        True if cancelled, False otherwise
    """
    return _cancellation_flags.get(incident_id, False)


def unregister_crash_task(incident_id: str) -> None:
    """
    Unregister a crash simulation task (cleanup).
    
    Args:
        incident_id: Incident identifier
    """
    if incident_id in _active_crash_tasks:
        del _active_crash_tasks[incident_id]
    if incident_id in _cancellation_flags:
        del _cancellation_flags[incident_id]
    logger.info("TASK_MANAGER", f"Unregistered crash task for incident: {incident_id}")


def get_active_incident_ids() -> list:
    """
    Get list of all active incident IDs.
    
    Returns:
        List of incident IDs with active simulations
    """
    return list(_active_crash_tasks.keys())


def cancel_all_simulations() -> int:
    """
    Cancel all active crash simulations.
    
    Returns:
        Number of simulations cancelled
    """
    count = 0
    for incident_id in list(_active_crash_tasks.keys()):
        if cancel_crash_simulation(incident_id):
            count += 1
    logger.warn("TASK_MANAGER", f"Cancelled all {count} active simulations")
    return count

