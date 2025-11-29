"""
Configuration and Settings

Environment variables and system-wide configuration for the trauma detection system.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # API Keys
    GOOGLE_MAPS_API_KEY: Optional[str] = None  # Get from https://console.cloud.google.com/apis/credentials
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_PHONE_NUMBER: Optional[str] = None
    SENDGRID_API_KEY: Optional[str] = None
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    
    # Emergency Services
    EMERGENCY_DISPATCHER_NUMBER: str = "108"  # Indian emergency number
    EMERGENCY_DISPATCHER_EMAIL: Optional[str] = None
    
    # Test Configuration (for real phone/email testing)
    FAMILY_PHONE: Optional[str] = None
    FAMILY_EMAIL: Optional[str] = None
    HOSPITAL_PHONE: Optional[str] = None
    HOSPITAL_EMAIL: Optional[str] = None
    
    # Detection Thresholds
    G_FORCE_THRESHOLD: float = 4.0
    HEART_RATE_SPIKE_THRESHOLD: float = 140.0
    HEART_RATE_DROP_THRESHOLD: float = 50.0
    VOICE_DECIBEL_THRESHOLD: float = 0.0
    
    # Financial
    DEFAULT_PREAUTH_AMOUNT: float = 50000.0  # ₹50,000
    PREAUTH_TOKEN_EXPIRY_HOURS: int = 24
    
    # GPS
    HOSPITAL_ARRIVAL_THRESHOLD_METERS: float = 100.0
    GPS_MONITORING_INTERVAL_SECONDS: float = 5.0
    
    # Timeouts
    CONSCIOUSNESS_TEST_DURATION_SECONDS: int = 5
    SWARM_ACTIVATION_TIMEOUT_SECONDS: int = 30
    
    # Application
    APP_NAME: str = "Trauma Detection System"
    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()

