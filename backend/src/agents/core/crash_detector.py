"""
Crash Detector - Phase 1: The "Triangulation" Trigger

This module implements the 3-confirmation system to prevent false alarms.
All three conditions must be met to confirm a CRITICAL EVENT:
1. Sensor Input: G-Force > 4G (Impact)
2. Biometric Check: Heart Rate spike (>140 BPM) followed by rapid drop or silence
3. Consciousness Test: No voice detected (voice_decibels == 0)
"""

from typing import Optional
from schemas.crash_payload import CrashPayloadInput
from utils.logger import logger


# Threshold constants
G_FORCE_THRESHOLD = 4.0  # G-Force threshold for impact detection
HEART_RATE_SPIKE_THRESHOLD = 140.0  # BPM threshold for shock detection
HEART_RATE_DROP_THRESHOLD = 50.0  # BPM threshold for unconsciousness
VOICE_DECIBEL_THRESHOLD = 0.0  # Decibel threshold for silence (no voice)


def check_impact(gforce: float) -> bool:
    """
    Check if accelerometer detects a significant impact.
    
    Args:
        gforce: Accelerometer G-Force reading
        
    Returns:
        True if G-Force > 4.0 (impact detected), False otherwise
        
    Example:
        >>> check_impact(5.2)
        True
        >>> check_impact(2.1)
        False
    """
    return gforce > G_FORCE_THRESHOLD


def check_heart_change(hr: float, hr_after: Optional[float]) -> bool:
    """
    Check for heart rate spike followed by rapid drop or silence.
    
    This detects the pattern: Heart Rate spike (>140 BPM) indicating shock,
    followed by either:
    - Rapid drop (<50 BPM) indicating unconsciousness
    - Silence (None) indicating no reading/sensor failure
    
    Args:
        hr: Initial heart rate reading (BPM)
        hr_after: Heart rate reading after impact (BPM). None indicates silence/no reading.
        
    Returns:
        True if heart rate spike detected AND (rapid drop OR silence), False otherwise
        
    Example:
        >>> check_heart_change(145.0, 45.0)  # Spike then drop
        True
        >>> check_heart_change(145.0, None)  # Spike then silence
        True
        >>> check_heart_change(80.0, 75.0)  # Normal, no spike
        False
        >>> check_heart_change(150.0, 120.0)  # Spike but no significant drop
        False
    """
    # Check for initial spike (shock response)
    has_spike = hr > HEART_RATE_SPIKE_THRESHOLD
    
    if not has_spike:
        return False
    
    # Check for rapid drop or silence (unconsciousness)
    if hr_after is None:
        # Silence - no reading detected (sensor failure or unconsciousness)
        return True
    
    # Rapid drop below threshold
    has_drop = hr_after < HEART_RATE_DROP_THRESHOLD
    
    return has_drop


def check_silence(decibels: float) -> bool:
    """
    Check if no voice was detected during consciousness test.
    
    The phone shouts "Impact detected. Speak to cancel." and listens for 5 seconds.
    If no voice is detected (decibels == 0), the user is considered unresponsive.
    
    Args:
        decibels: Voice decibel level detected during consciousness test
        
    Returns:
        True if voice_decibels == 0 (no voice detected), False otherwise
        
    Example:
        >>> check_silence(0.0)
        True
        >>> check_silence(45.2)
        False
    """
    return decibels == VOICE_DECIBEL_THRESHOLD


def triangulate(payload: CrashPayloadInput) -> tuple[bool, str]:
    """
    The "Triangulation" Trigger - Requires 3 confirmations to prevent false alarms.
    
    This is Phase 1 of the trauma detection system. All three conditions must be met:
    1. Sensor Input: G-Force > 4G (Impact)
    2. Biometric Check: Heart Rate spike (>140 BPM) followed by rapid drop or silence
    3. Consciousness Test: No voice detected (voice_decibels == 0)
    
    Args:
        payload: CrashPayloadInput containing all sensor data and user information
        
    Returns:
        Tuple of (is_critical: bool, status: str)
        - is_critical: True if all 3 confirmations are met (CRITICAL EVENT CONFIRMED)
        - status: Status message describing the result
        
    Example:
        >>> payload = CrashPayloadInput(
        ...     g_force=5.2,
        ...     heart_rate=145.0,
        ...     heart_rate_after=45.0,
        ...     voice_decibels=0.0,
        ...     gps=GPSLocation(lat=19.1680, lon=72.8500),  # NESCO Centre Goregaon
        ...     blood_type="O+",
        ...     allergies=["Penicillin"],
        ...     user_consent=True
        ... )
        >>> triangulate(payload)
        (True, "CRITICAL_EVENT_CONFIRMED")
    """
    # Check user consent first
    if not payload.user_consent:
        logger.warn("TRIANGULATION", "User consent not provided")
        return False, "MONITOR_MODE - User consent not provided"
    
    # Confirmation 1: Impact Detection (G-Force > 4.0)
    impact_detected = check_impact(payload.g_force)
    if impact_detected:
        logger.info("TRIANGULATION", f"✅ Confirmation 1: Impact detected (G-Force: {payload.g_force}G > {G_FORCE_THRESHOLD}G)")
    else:
        logger.info("TRIANGULATION", f"❌ Confirmation 1: Impact threshold not met (G-Force: {payload.g_force}G <= {G_FORCE_THRESHOLD}G)")
    
    # Confirmation 2: Heart Rate Change (Spike >140 BPM then drop <50 BPM OR flatline)
    heart_change_detected = check_heart_change(
        payload.heart_rate, 
        payload.heart_rate_after
    )
    if heart_change_detected:
        logger.info("TRIANGULATION", f"✅ Confirmation 2: Heart rate spike detected (HR: {payload.heart_rate} BPM > {HEART_RATE_SPIKE_THRESHOLD} BPM) → drop ({payload.heart_rate_after} BPM < {HEART_RATE_DROP_THRESHOLD} BPM or silence)")
    else:
        logger.info("TRIANGULATION", f"❌ Confirmation 2: Heart rate pattern not detected (HR: {payload.heart_rate} → {payload.heart_rate_after})")
    
    # Confirmation 3: Silence (No Voice Response - voice_decibels == 0)
    silence_detected = check_silence(payload.voice_decibels)
    if silence_detected:
        logger.info("TRIANGULATION", f"✅ Confirmation 3: No voice detected (Decibels: {payload.voice_decibels} == {VOICE_DECIBEL_THRESHOLD})")
    else:
        logger.info("TRIANGULATION", f"❌ Confirmation 3: Voice detected (Decibels: {payload.voice_decibels} != {VOICE_DECIBEL_THRESHOLD})")
    
    # All 3 confirmations required
    if impact_detected and heart_change_detected and silence_detected:
        logger.critical("TRIANGULATION", "✅ ALL 3 CONFIRMATIONS MET → CRITICAL EVENT CONFIRMED")
        return True, "CRITICAL_EVENT_CONFIRMED"
    
    # Build detailed status message for debugging
    status_parts = []
    if not impact_detected:
        status_parts.append(f"Impact threshold not met (G-Force: {payload.g_force}G)")
    if not heart_change_detected:
        status_parts.append(f"Heart rate pattern not detected (HR: {payload.heart_rate} -> {payload.heart_rate_after})")
    if not silence_detected:
        status_parts.append(f"Voice detected (Decibels: {payload.voice_decibels})")
    
    status = "MONITOR_MODE - " + "; ".join(status_parts)
    logger.warn("TRIANGULATION", f"Triangulation failed: {status}")
    return False, status
