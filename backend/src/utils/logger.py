"""
Professional Logging System for Emergency Response

Provides timestamped logging in the format: [HH:MM:SS.mmm] AGENT → Message
"""

from datetime import datetime
from typing import Optional
import sys


class EmergencyLogger:
    """
    Black-ops style logger for emergency response system.
    
    Format: [HH:MM:SS.mmm] AGENT → Message
    """
    
    def __init__(self):
        self.start_time = datetime.now()
    
    def _get_timestamp(self) -> str:
        """Get formatted timestamp relative to system start"""
        now = datetime.now()
        elapsed = (now - self.start_time).total_seconds()
        
        hours = int(elapsed // 3600)
        minutes = int((elapsed % 3600) // 60)
        seconds = int(elapsed % 60)
        milliseconds = int((elapsed % 1) * 1000)
        
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"
    
    def log(self, agent: str, message: str, level: str = "INFO"):
        """
        Log a message with timestamp and agent identifier.
        
        Args:
            agent: Agent name (e.g., "AGENT A", "GUARDIAN", "TREASURER")
            message: Log message
            level: Log level (INFO, WARN, ERROR, CRITICAL)
        """
        timestamp = self._get_timestamp()
        
        # Color codes for different levels
        colors = {
            "INFO": "",
            "WARN": "\033[93m",  # Yellow
            "ERROR": "\033[91m",  # Red
            "CRITICAL": "\033[95m",  # Magenta
            "SUCCESS": "\033[92m"  # Green
        }
        reset = "\033[0m"
        
        color = colors.get(level, "")
        # Use ASCII-safe arrow for Windows compatibility
        arrow = "->"
        try:
            log_line = f"[{timestamp}] {color}{agent} → {message}{reset}"
            print(log_line, file=sys.stderr if level in ["ERROR", "CRITICAL"] else sys.stdout)
        except UnicodeEncodeError:
            # Fallback to ASCII if encoding fails (Windows console)
            log_line = f"[{timestamp}] {color}{agent} {arrow} {message}{reset}"
            print(log_line, file=sys.stderr if level in ["ERROR", "CRITICAL"] else sys.stdout)
        sys.stdout.flush()
    
    def info(self, agent: str, message: str):
        """Log info message"""
        self.log(agent, message, "INFO")
    
    def warn(self, agent: str, message: str):
        """Log warning message"""
        self.log(agent, message, "WARN")
    
    def error(self, agent: str, message: str):
        """Log error message"""
        self.log(agent, message, "ERROR")
    
    def critical(self, agent: str, message: str):
        """Log critical message"""
        self.log(agent, message, "CRITICAL")
    
    def success(self, agent: str, message: str):
        """Log success message"""
        self.log(agent, message, "SUCCESS")


# Global logger instance
logger = EmergencyLogger()

