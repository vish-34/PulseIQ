"""
Master Agent Orchestrator

Orchestrates all 3 sub-agents (Dispatcher, Guardian, Treasurer) in parallel.
This is Phase 2: The Multi-Agent Swarm (10-30 seconds).
"""

import asyncio
from typing import Dict, Any
from schemas.crash_payload import CrashPayloadInput
from agents.core.state_machine import IncidentState
from agents.dispatcher.dispatcher_agent import run as dispatcher_run
from agents.guardian.guardian_agent import run as guardian_run
from agents.treasurer.treasurer_agent import run as treasurer_run
from config.settings import settings
from utils.logger import logger


async def activate_swarm(
    payload: CrashPayloadInput,
    incident_id: str,
    incident_state: IncidentState
) -> Dict[str, Any]:
    """
    Activate the multi-agent swarm - all 3 agents run in parallel.
    
    This is the core of Phase 2. The Master Agent wakes up:
    - Agent A: The Dispatcher (Logistics)
    - Agent B: The Guardian (Medical Data)
    - Agent C: The Treasurer (Financial)
    
    All agents execute simultaneously for maximum speed.
    
    Args:
        payload: Crash payload input
        incident_id: Incident identifier
        incident_state: State machine instance
        
    Returns:
        Dictionary with aggregated results:
        {
            "success": bool,
            "dispatcher_result": dict,
            "guardian_result": dict,
            "treasurer_result": dict,
            "execution_time_seconds": float,
            "message": str
        }
    """
    logger.critical("MASTER_AGENT", "🚨 ACTIVATING MULTI-AGENT SWARM 🚨")
    logger.info("MASTER_AGENT", f"Incident ID: {incident_id}")
    logger.info("MASTER_AGENT", "Starting parallel execution of 3 agents (NO sequential fallback)")
    
    start_time = asyncio.get_event_loop().time()
    
    result = {
        "success": False,
        "dispatcher_result": {},
        "guardian_result": {},
        "treasurer_result": {},
        "execution_time_seconds": 0.0,
        "message": ""
    }
    
    try:
        # Run all 3 agents in parallel using asyncio.gather
        logger.info("MASTER_AGENT", "Firing Agent A (Dispatcher) - Logistics")
        logger.info("MASTER_AGENT", "Firing Agent B (Guardian) - Medical")
        logger.info("MASTER_AGENT", "Firing Agent C (Treasurer) - Financial")
        logger.info("MASTER_AGENT", "All agents running in parallel (asyncio.gather)")
        
        # Create tasks for parallel execution
        dispatcher_task = dispatcher_run(payload, incident_id)
        guardian_task = guardian_run(payload, incident_id)
        
        # Treasurer needs hospital info, so we'll get it from dispatcher first
        # For true parallel execution, we'll start treasurer with None and update later
        treasurer_task = treasurer_run(payload, incident_id, None)
        
        # Execute all tasks in parallel with timeout
        try:
            dispatcher_result, guardian_result, treasurer_result = await asyncio.wait_for(
                asyncio.gather(
                    dispatcher_task,
                    guardian_task,
                    treasurer_task,
                    return_exceptions=True
                ),
                timeout=settings.SWARM_ACTIVATION_TIMEOUT_SECONDS
            )
        except asyncio.TimeoutError:
            logger.error("MASTER_AGENT", f"⚠️ WARNING: Swarm activation timed out after {settings.SWARM_ACTIVATION_TIMEOUT_SECONDS}s!")
            result["message"] = "Swarm activation timed out"
            return result
        
        # Handle exceptions from agents
        if isinstance(dispatcher_result, Exception):
            logger.error("MASTER_AGENT", f"Agent A error: {dispatcher_result}")
            dispatcher_result = {"success": False, "error": str(dispatcher_result)}
        
        if isinstance(guardian_result, Exception):
            logger.error("MASTER_AGENT", f"Agent B error: {guardian_result}")
            guardian_result = {"success": False, "error": str(guardian_result)}
        
        if isinstance(treasurer_result, Exception):
            logger.error("MASTER_AGENT", f"Agent C error: {treasurer_result}")
            treasurer_result = {"success": False, "error": str(treasurer_result)}
        
        result["dispatcher_result"] = dispatcher_result
        result["guardian_result"] = guardian_result
        result["treasurer_result"] = treasurer_result
        
        # If dispatcher found hospital, update treasurer with hospital info
        if dispatcher_result.get("success") and dispatcher_result.get("hospital"):
            hospital_info = dispatcher_result["hospital"]
            logger.info("MASTER_AGENT", "Updating Treasurer with hospital info from Dispatcher")
            # Re-run treasurer with hospital info (or update in real system)
            updated_treasurer = await treasurer_run(
                payload,
                incident_id,
                hospital_info
            )
            if updated_treasurer.get("success"):
                result["treasurer_result"] = updated_treasurer
        
        # Calculate execution time
        end_time = asyncio.get_event_loop().time()
        execution_time = end_time - start_time
        result["execution_time_seconds"] = round(execution_time, 2)
        
        # Determine overall success
        all_success = (
            dispatcher_result.get("success", False) and
            guardian_result.get("success", False) and
            treasurer_result.get("success", False)
        )
        
        result["success"] = all_success
        
        # Log results
        logger.success("MASTER_AGENT", f"🎯 SWARM ACTIVATION COMPLETE - Execution time: {execution_time:.2f}s")
        logger.info("MASTER_AGENT", f"Agent A (Dispatcher): {'✅ SUCCESS' if dispatcher_result.get('success') else '❌ FAILED'}")
        logger.info("MASTER_AGENT", f"Agent B (Guardian): {'✅ SUCCESS' if guardian_result.get('success') else '❌ FAILED'}")
        logger.info("MASTER_AGENT", f"Agent C (Treasurer): {'✅ SUCCESS' if treasurer_result.get('success') else '❌ FAILED'}")
        
        if all_success:
            result["message"] = "All agents completed successfully"
            logger.success("MASTER_AGENT", "All 3 agents completed successfully in parallel")
        else:
            result["message"] = "Some agents encountered errors"
            logger.warn("MASTER_AGENT", "Some agents encountered errors")
        
    except Exception as e:
        result["message"] = f"Master agent error: {str(e)}"
        logger.error("MASTER_AGENT", f"❌ CRITICAL ERROR: {e}")
    
    return result


async def handle_phase_2(
    payload: CrashPayloadInput,
    incident_id: str,
    incident_state: IncidentState
) -> Dict[str, Any]:
    """
    Main entry point for Phase 2: Multi-Agent Swarm.
    
    This function:
    1. Activates the swarm
    2. Updates state machine to 'dispatching'
    3. Returns results
    
    Args:
        payload: Crash payload input
        incident_id: Incident identifier
        incident_state: State machine instance
        
    Returns:
        Dictionary with Phase 2 results
    """
    # Update state machine
    if incident_state.state == "CriticalConfirmed":
        incident_state.activate_protocol()
    
    # Activate swarm
    swarm_result = await activate_swarm(payload, incident_id, incident_state)
    
    # Update metadata in state machine
    incident_state.update_metadata("swarm_result", swarm_result)
    
    return swarm_result

