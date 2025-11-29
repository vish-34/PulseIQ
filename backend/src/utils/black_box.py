"""
Black Box Recording System

Implements continuous audio recording with rolling 60-second buffer for legal evidence.
"""

import asyncio
from datetime import datetime
from typing import Dict, Any, Optional
from collections import deque
from utils.logger import logger


class BlackBoxRecorder:
    """
    Black Box recorder with rolling 60-second buffer.
    
    Continuously records audio and maintains a rolling buffer of the last 60 seconds.
    All recordings are timestamped and tagged with incident ID.
    """
    
    def __init__(self, incident_id: str, buffer_duration_seconds: int = 60):
        """
        Initialize black box recorder.
        
        Args:
            incident_id: Incident identifier
            buffer_duration_seconds: Duration of rolling buffer (default 60 seconds)
        """
        self.incident_id = incident_id
        self.buffer_duration = buffer_duration_seconds
        self.is_recording = False
        self.recording_id = f"recording_{incident_id}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        self.buffer: deque = deque(maxlen=buffer_duration_seconds)  # Rolling buffer
        self.start_time: Optional[datetime] = None
        self.recording_task: Optional[asyncio.Task] = None
        
        logger.info("BLACK_BOX", f"Recorder initialized: {self.recording_id}")
    
    async def start_recording(self) -> str:
        """
        Start continuous audio recording in Black Box mode.
        
        Returns:
            Recording ID
        """
        if self.is_recording:
            logger.warn("BLACK_BOX", "Recording already in progress")
            return self.recording_id
        
        self.is_recording = True
        self.start_time = datetime.utcnow()
        
        logger.info("BLACK_BOX", f"Recording started - Incident: {self.incident_id}")
        logger.info("BLACK_BOX", f"Rolling buffer: {self.buffer_duration} seconds")
        
        # Start recording task
        self.recording_task = asyncio.create_task(self._record_loop())
        
        return self.recording_id
    
    async def _record_loop(self):
        """
        Internal recording loop - simulates continuous audio capture.
        
        In production, this would:
        - Capture audio from device microphone
        - Store chunks in secure location
        - Maintain rolling buffer
        """
        chunk_index = 0
        max_demo_duration = 60  # Auto-stop after 60 seconds for demo
        last_log_time = datetime.utcnow()
        
        while self.is_recording:
            # Check if we should auto-stop (for demo purposes)
            if self.start_time:
                elapsed = (datetime.utcnow() - self.start_time).total_seconds()
                if elapsed >= max_demo_duration:
                    logger.info("BLACK_BOX", f"Auto-stopping recording after {max_demo_duration}s (demo mode)")
                    self.is_recording = False
                    break
            
            # Simulate audio chunk capture
            chunk = {
                "timestamp": datetime.utcnow().isoformat(),
                "chunk_index": chunk_index,
                "incident_id": self.incident_id,
                "data": f"audio_chunk_{chunk_index}",  # In production: actual audio bytes
                "duration_ms": 100  # 100ms chunks
            }
            
            # Add to rolling buffer
            self.buffer.append(chunk)
            
            # Log only every 10 seconds (100 chunks) to reduce noise
            current_time = datetime.utcnow()
            if (current_time - last_log_time).total_seconds() >= 10:
                logger.info("BLACK_BOX", f"Recording active - Buffer: {len(self.buffer)}/{self.buffer_duration} seconds (chunk {chunk_index})")
                last_log_time = current_time
            
            chunk_index += 1
            await asyncio.sleep(0.1)  # 100ms intervals
    
    async def stop_recording(self) -> Dict[str, Any]:
        """
        Stop recording and return final buffer.
        
        Returns:
            Dictionary with recording metadata and buffer
        """
        if not self.is_recording:
            logger.warn("BLACK_BOX", "No recording in progress")
            return {}
        
        self.is_recording = False
        
        if self.recording_task:
            self.recording_task.cancel()
            try:
                await self.recording_task
            except asyncio.CancelledError:
                pass
        
        end_time = datetime.utcnow()
        duration = (end_time - self.start_time).total_seconds() if self.start_time else 0
        
        result = {
            "recording_id": self.recording_id,
            "incident_id": self.incident_id,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": end_time.isoformat(),
            "duration_seconds": duration,
            "buffer_chunks": len(self.buffer),
            "buffer_duration_seconds": self.buffer_duration
        }
        
        logger.info("BLACK_BOX", f"Recording stopped - Duration: {duration:.2f}s, Chunks: {len(self.buffer)}")
        
        return result
    
    def get_buffer(self) -> list:
        """
        Get current rolling buffer contents.
        
        Returns:
            List of audio chunks in buffer
        """
        return list(self.buffer)
    
    def get_status(self) -> Dict[str, Any]:
        """
        Get current recording status.
        
        Returns:
            Dictionary with recording status
        """
        return {
            "recording_id": self.recording_id,
            "incident_id": self.incident_id,
            "is_recording": self.is_recording,
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "buffer_size": len(self.buffer),
            "buffer_duration_seconds": self.buffer_duration
        }


# Global recorder instances (in production, use proper storage)
_active_recorders: Dict[str, BlackBoxRecorder] = {}


def start_black_box_recording(incident_id: str) -> BlackBoxRecorder:
    """
    Start black box recording for an incident.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        BlackBoxRecorder instance
    """
    recorder = BlackBoxRecorder(incident_id)
    _active_recorders[incident_id] = recorder
    
    # Start recording asynchronously
    # Note: The recording will run in the background and auto-stop after 60 seconds (demo mode)
    try:
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # Create task in running event loop
            loop.create_task(recorder.start_recording())
        else:
            # No running loop, create one
            asyncio.run(recorder.start_recording())
    except RuntimeError:
        # No event loop exists, create one
        asyncio.run(recorder.start_recording())
    
    return recorder


async def stop_black_box_recording(incident_id: str) -> Optional[Dict[str, Any]]:
    """
    Stop black box recording for an incident.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        Recording metadata or None if not found
    """
    recorder = _active_recorders.get(incident_id)
    if recorder:
        result = await recorder.stop_recording()
        _active_recorders.pop(incident_id, None)
        return result
    return None


def get_recorder(incident_id: str) -> Optional[BlackBoxRecorder]:
    """
    Get active recorder for an incident.
    
    Args:
        incident_id: Incident identifier
        
    Returns:
        BlackBoxRecorder instance or None
    """
    return _active_recorders.get(incident_id)

