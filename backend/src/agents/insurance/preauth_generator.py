"""
Pre-Authorization Token Generator

Generates unique pre-authorization tokens for hospital admission.
"""

import uuid
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from config.settings import settings

# In-memory token storage (in production, use database)
TOKEN_STORAGE: Dict[str, Dict[str, Any]] = {}


async def generate_preauth_token(
    policy_number: str,
    amount: float,
    hospital_id: str,
    incident_id: str
) -> str:
    """
    Generate a unique pre-authorization token.
    
    Args:
        policy_number: Insurance policy number
        amount: Pre-authorized amount (₹)
        hospital_id: Hospital identifier
        incident_id: Incident identifier
        
    Returns:
        Pre-authorization token string
        Format: PREAUTH_{YYYYMMDD}_{RANDOM6}
    """
    # Generate token components
    date_str = datetime.utcnow().strftime("%Y%m%d")
    random_part = uuid.uuid4().hex[:6].upper()
    
    token = f"PREAUTH_{date_str}_{random_part}"
    
    # Calculate expiry
    expires_at = datetime.utcnow() + timedelta(hours=settings.PREAUTH_TOKEN_EXPIRY_HOURS)
    
    # Store token information
    TOKEN_STORAGE[token] = {
        "token": token,
        "policy_number": policy_number,
        "amount": amount,
        "hospital_id": hospital_id,
        "incident_id": incident_id,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": expires_at.isoformat(),
        "used": False
    }
    
    return token


async def validate_token(token: str) -> Dict[str, Any]:
    """
    Validate a pre-authorization token.
    
    Args:
        token: Pre-authorization token to validate
        
    Returns:
        Dictionary containing validation result:
        {
            "valid": bool,
            "amount": float,
            "hospital_id": str,
            "expires_at": str,
            "used": bool,
            "message": str
        }
    """
    if token not in TOKEN_STORAGE:
        return {
            "valid": False,
            "amount": 0.0,
            "hospital_id": "",
            "expires_at": "",
            "used": False,
            "message": "Token not found"
        }
    
    token_data = TOKEN_STORAGE[token]
    expires_at = datetime.fromisoformat(token_data["expires_at"])
    
    # Check if expired
    if datetime.utcnow() > expires_at:
        return {
            "valid": False,
            "amount": token_data["amount"],
            "hospital_id": token_data["hospital_id"],
            "expires_at": token_data["expires_at"],
            "used": token_data["used"],
            "message": "Token has expired"
        }
    
    # Check if already used
    if token_data["used"]:
        return {
            "valid": False,
            "amount": token_data["amount"],
            "hospital_id": token_data["hospital_id"],
            "expires_at": token_data["expires_at"],
            "used": True,
            "message": "Token has already been used"
        }
    
    return {
        "valid": True,
        "amount": token_data["amount"],
        "hospital_id": token_data["hospital_id"],
        "expires_at": token_data["expires_at"],
        "used": False,
        "message": "Token is valid"
    }


async def mark_token_used(token: str) -> bool:
    """
    Mark a token as used.
    
    Args:
        token: Pre-authorization token
        
    Returns:
        True if token was marked as used, False if not found
    """
    if token in TOKEN_STORAGE:
        TOKEN_STORAGE[token]["used"] = True
        return True
    return False

