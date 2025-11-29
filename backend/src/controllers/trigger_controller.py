"""
Trigger Controller - Handles crash detection trigger endpoint

Main entry point for crash detection and emergency response activation.
"""

from datetime import datetime
from typing import Dict, Any
from schemas.crash_payload import CrashPayloadInput, CrashPayloadOutput, GPSLocation
from agents.core.crash_detector import triangulate
from agents.core.state_machine import IncidentState, create_incident_state
from agents.core.master_agent import handle_phase_2
from models.incident_model import new_incident
from utils.id_generator import generate_incident_id
from utils.logger import logger
from utils.crash_task_manager import register_crash_task, is_cancelled, unregister_crash_task
import asyncio


async def handle_crash_trigger(payload: CrashPayloadInput) -> CrashPayloadOutput:
    """
    Handle crash detection trigger - Main flow controller.
    
    Flow:
    1. Validate payload
    2. Create incident
    3. Initialize state machine
    4. Run triangulation (Phase 1)
    5. If confirmed: activate Phase 2 (Multi-Agent Swarm)
    6. Return response
    
    Args:
        payload: Crash payload input
        
    Returns:
        CrashPayloadOutput with incident details
    """
    logger.critical("SYSTEM", "="*70)
    logger.critical("SYSTEM", "🚨 CRASH DETECTION TRIGGERED 🚨")
    logger.critical("SYSTEM", "="*70)
    
    # Step 1: Generate incident ID
    incident_id = generate_incident_id()
    logger.info("SYSTEM", f"Incident ID: {incident_id}")
    logger.info("SYSTEM", "Starting crash detection and emergency response protocol...")
    
    # Register this task for potential cancellation
    current_task = asyncio.current_task()
    if current_task:
        register_crash_task(incident_id, current_task)
    
    # Step 2: Create incident record
    incident_data = {
        "incident_id": incident_id,
        "payload": payload.dict(),
        "created_at": datetime.utcnow().isoformat()
    }
    incident = new_incident(incident_data)
    
    # Step 3: Initialize state machine
    incident_state = create_incident_state(incident_id)
    incident_state.set_payload(payload)
    
    # Step 4: Start monitoring (Idle -> Monitoring)
    incident_state.start_monitoring(payload)
    logger.info("SYSTEM", f"State: {incident_state.state}")
    
    # Step 5: Run triangulation (Phase 1) - Check ALL 3 conditions
    logger.info("PHASE_1", "="*70)
    logger.info("PHASE_1", "Running triangulation - Checking 3 confirmations:")
    logger.info("PHASE_1", "1. G-Force listener: Checking impact > 4.0G")
    logger.info("PHASE_1", "2. Heart-rate listener: Checking spike >140 BPM then drop <50 BPM or flatline")
    logger.info("PHASE_1", "3. Microphone listener: Checking voice detection (5 seconds)")
    logger.info("PHASE_1", f"Payload values: G-Force={payload.g_force}, HR={payload.heart_rate}, HR_after={payload.heart_rate_after}, Voice={payload.voice_decibels}")
    
    try:
        is_critical, status = triangulate(payload)
        logger.info("PHASE_1", f"Triangulation completed: is_critical={is_critical}, status={status}")
    except Exception as e:
        import traceback
        logger.error("PHASE_1", f"ERROR in triangulation: {e}")
        logger.error("PHASE_1", f"Traceback: {traceback.format_exc()}")
        raise
    
    if not is_critical:
        # Not a critical event - return early
        logger.warn("PHASE_1", "="*70)
        logger.warn("PHASE_1", f"⚠️ NOT CRITICAL - Triangulation result: {status}")
        logger.warn("PHASE_1", "Returning early - crash simulation will NOT continue")
        logger.warn("PHASE_1", "="*70)
        return CrashPayloadOutput(
            incident_id=incident_id,
            status=status,
            gps=payload.gps,
            timestamp=datetime.utcnow().isoformat()
        )
    
    logger.info("PHASE_1", "✅ All 3 confirmations met - Proceeding with crash simulation")
    
    # Step 6: Start triangulation pending (consciousness test)
    logger.info("PHASE_1", f"Triangulation result: {status}")
    incident_state.start_triangulation()
    logger.info("PHASE_1", f"State: {incident_state.state}")
    logger.info("PHASE_1", "Consciousness test: Device says 'Impact detected. Speak to cancel.' - Listening for 5 seconds...")
    logger.info("PHASE_1", "NOTE: Stop button can cancel this simulation during this 5-second window")
    
    # Simulate 5-second wait (in real system, this would be actual voice detection)
    # Check for cancellation every 0.5 seconds
    for _ in range(10):  # 10 * 0.5s = 5 seconds
        if is_cancelled(incident_id):
            logger.warn("PHASE_1", "="*70)
            logger.warn("PHASE_1", "⚠️ CRASH SIMULATION CANCELLED BY STOP BUTTON ⚠️")
            logger.warn("PHASE_1", f"Incident ID: {incident_id}")
            logger.warn("PHASE_1", "="*70)
            incident_state.cancel_incident("Cancelled by stop button during consciousness test")
            unregister_crash_task(incident_id)
            raise asyncio.CancelledError("Crash simulation cancelled by stop button")
        await asyncio.sleep(0.5)
    
    # Step 7: Confirm critical event (no voice detected)
    incident_state.confirm_critical_event()
    logger.critical("PHASE_1", "✅ CRITICAL EVENT CONFIRMED - All 3 confirmations met, no voice detected")
    logger.info("PHASE_1", f"State: {incident_state.state}")
    
    # Step 7.5: Notify family immediately after crash confirmation
    logger.info("PHASE_1", "Notifying family: Crash detected, emergency services being dispatched")
    from utils.family_notifications import notify_family_crash_alert
    family_notification_result = await notify_family_crash_alert(
        incident_id=incident_id,
        gps_lat=payload.gps.lat,
        gps_lon=payload.gps.lon,
        blood_type=payload.blood_type
    )
    if family_notification_result.get("success"):
        logger.success("PHASE_1", "Family notified: Email, Call, and SMS sent")
    else:
        logger.warn("PHASE_1", "Family notification partially failed - check logs")
    
    logger.info("PHASE_1", "Moving to Phase 2: Multi-Agent Swarm (10-30 seconds)")
    
    # Step 8: Activate Phase 2 - Multi-Agent Swarm
    swarm_result = await handle_phase_2(payload, incident_id, incident_state)
    
    # Step 9: Build response
    hospital_info = swarm_result.get("dispatcher_result", {}).get("hospital")
    preauth_token = swarm_result.get("treasurer_result", {}).get("preauth_token")
    
    output = CrashPayloadOutput(
        incident_id=incident_id,
        status="PROTOCOL_ACTIVE",
        gps=payload.gps,
        nearest_hospital=hospital_info,
        ambulance_dispatched=swarm_result.get("dispatcher_result", {}).get("ambulance_dispatched", False),
        insurance_preauth_token=preauth_token,
        family_notified=family_notification_result.get("success", False),  # Updated from Phase 1
        timestamp=datetime.utcnow().isoformat()
    )
    
    logger.success("SYSTEM", "✅ Phase 2 finished - Simulating ambulance transport to hospital")
    
    # Step 10: Simulate 30-second transport to hospital, then trigger Phase 3
    logger.info("PHASE_3", "Simulating ambulance transport to hospital (30 seconds)...")
    logger.info("PHASE_3", "Ambulance is en route to hospital...")
    logger.info("PHASE_3", "NOTE: Stop button can cancel this simulation during transport")
    
    # Wait 30 seconds to simulate transport, checking for cancellation every 1 second
    for _ in range(30):  # 30 * 1s = 30 seconds
        if is_cancelled(incident_id):
            logger.warn("PHASE_3", "="*70)
            logger.warn("PHASE_3", "⚠️ CRASH SIMULATION CANCELLED BY STOP BUTTON ⚠️")
            logger.warn("PHASE_3", f"Incident ID: {incident_id}")
            logger.warn("PHASE_3", "="*70)
            unregister_crash_task(incident_id)
            raise asyncio.CancelledError("Crash simulation cancelled by stop button during transport")
        await asyncio.sleep(1)
    
    # Step 11: Trigger Phase 3 - Hospital Arrival
    logger.info("PHASE_3", "Ambulance has arrived at hospital - Triggering Phase 3: Hospital Arrival Handoff")
    
    # Get hospital GPS from hospital info
    if hospital_info and hospital_info.get("gps"):
        hospital_gps = GPSLocation(
            lat=hospital_info["gps"].get("lat", payload.gps.lat),
            lon=hospital_info["gps"].get("lon", payload.gps.lon)
        )
    else:
        # Use a nearby location as hospital (for demo)
        hospital_gps = GPSLocation(
            lat=payload.gps.lat + 0.01,  # Slightly different location
            lon=payload.gps.lon + 0.01
        )
    
    hospital_name = hospital_info.get("name", "City Trauma Center") if hospital_info else "City Trauma Center"
    
    # Trigger hospital arrival handoff
    from utils.geofence import handle_hospital_arrival
    arrival_result = await handle_hospital_arrival(
        incident_id=incident_id,
        incident_state=incident_state,
        hospital_gps=hospital_gps,
        hospital_name=hospital_name
    )
    
    if arrival_result.get("success"):
        logger.success("SYSTEM", "✅ Phase 3 complete - Hospital arrival handoff finished")
        logger.success("SYSTEM", "Family notified again: Email, Call, and SMS sent for hospital arrival")
    else:
        logger.warn("SYSTEM", "Phase 3 partially completed - check logs")
    
    # Stop black box recording after Phase 3 completes
    from utils.black_box import stop_black_box_recording
    try:
        await stop_black_box_recording(incident_id)
        logger.info("SYSTEM", "Black Box recording stopped after Phase 3 completion")
    except Exception as e:
        logger.warn("SYSTEM", f"Could not stop black box recording: {e}")
    
    # Update output with final status (create new output with updated values)
    final_output = CrashPayloadOutput(
        incident_id=output.incident_id,
        status="HOSPITAL_ARRIVED",
        gps=output.gps,
        nearest_hospital=output.nearest_hospital,
        ambulance_dispatched=output.ambulance_dispatched,
        insurance_preauth_token=output.insurance_preauth_token,
        family_notified=arrival_result.get("family_notified", output.family_notified),
        timestamp=output.timestamp
    )
    
    logger.success("SYSTEM", "✅ COMPLETE INCIDENT PROCESSING - All phases finished")
    logger.success("SYSTEM", "📞 Two calls made: 1) Crash alert, 2) Hospital arrival")
    
    # Cleanup: Unregister task
    unregister_crash_task(incident_id)
    
    return final_output

