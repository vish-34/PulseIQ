"""
Crash Payload Schema Definitions

This module defines the input and output schemas for the trauma detection system.
All schemas use Pydantic for validation and type safety.
"""

from typing import Optional, List
from pydantic import BaseModel, Field, field_validator


class GPSLocation(BaseModel):
    """GPS coordinates for location tracking"""
    lat: float = Field(..., description="Latitude coordinate", ge=-90, le=90)
    lon: float = Field(..., description="Longitude coordinate", ge=-180, le=180)


class CrashPayloadInput(BaseModel):
    """
    Input schema for crash detection payload.
    This represents the raw sensor data received from devices.
    """
    g_force: float = Field(
        ..., 
        description="Accelerometer G-Force reading (impact detection)",
        gt=0
    )
    
    heart_rate: float = Field(
        ..., 
        description="Initial heart rate reading from smartwatch (BPM)",
        gt=0,
        le=300
    )
    
    heart_rate_after: Optional[float] = Field(
        None,
        description="Heart rate reading after impact (BPM). None indicates no reading/silence",
        gt=0,
        le=300
    )
    
    voice_decibels: float = Field(
        ..., 
        description="Voice decibel level detected during consciousness test (0 = no voice)",
        ge=0
    )
    
    gps: GPSLocation = Field(
        ..., 
        description="GPS coordinates of the crash location"
    )
    
    blood_type: str = Field(
        ..., 
        description="User's blood type (e.g., 'O+', 'A-', 'B+', 'AB-')",
        pattern="^(A|B|AB|O)[+-]$"
    )
    
    allergies: List[str] = Field(
        default_factory=list,
        description="List of known allergies (e.g., ['Penicillin', 'Latex'])"
    )
    
    user_consent: bool = Field(
        ..., 
        description="User consent for automated emergency response"
    )
    
    @field_validator('heart_rate_after')
    @classmethod
    def validate_heart_rate_after(cls, v, info):
        """Validate that heart_rate_after is less than or equal to initial heart_rate if provided"""
        if v is not None:
            # Allow for spike then drop scenario
            pass
        return v


class CrashPayloadOutput(BaseModel):
    """
    Output schema for crash detection response.
    This represents the processed response after protocol activation.
    """
    incident_id: str = Field(
        ..., 
        description="Unique identifier for this incident"
    )
    
    status: str = Field(
        ..., 
        description="Status of the incident (e.g., 'CRITICAL_EVENT_CONFIRMED', 'PROTOCOL_ACTIVE')"
    )
    
    gps: GPSLocation = Field(
        ..., 
        description="GPS coordinates where the crash was detected"
    )
    
    nearest_hospital: Optional[dict] = Field(
        None,
        description="Information about the nearest trauma center"
    )
    
    ambulance_dispatched: bool = Field(
        default=False,
        description="Whether ambulance has been dispatched"
    )
    
    insurance_preauth_token: Optional[str] = Field(
        None,
        description="Pre-authorization token for hospital admission"
    )
    
    family_notified: bool = Field(
        default=False,
        description="Whether family has been notified"
    )
    
    timestamp: str = Field(
        ..., 
        description="ISO format timestamp of when the incident was detected"
    )


class SensorData(BaseModel):
    """
    Real-time sensor data model for continuous monitoring.
    """
    g_force: float = Field(..., description="Current G-Force reading", gt=0)
    heart_rate: float = Field(..., description="Current heart rate (BPM)", gt=0, le=300)
    voice_decibels: float = Field(..., description="Current voice decibel level", ge=0)
    gps: GPSLocation = Field(..., description="Current GPS coordinates")
    timestamp: str = Field(..., description="ISO format timestamp of sensor reading")


class UserMedicalProfile(BaseModel):
    """
    User's medical profile for emergency responders.
    """
    blood_type: str = Field(
        ..., 
        description="Blood type",
        pattern="^(A|B|AB|O)[+-]$"
    )
    
    allergies: List[str] = Field(
        default_factory=list,
        description="List of known allergies"
    )
    
    medical_conditions: Optional[List[str]] = Field(
        default_factory=list,
        description="Pre-existing medical conditions"
    )
    
    emergency_contact: Optional[str] = Field(
        None,
        description="Emergency contact phone number"
    )
    
    insurance_policy_number: Optional[str] = Field(
        None,
        description="Insurance policy number for pre-authorization"
    )

