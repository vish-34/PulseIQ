"""
ID Generator - Generate unique incident IDs
"""

import uuid
from datetime import datetime


def generate_incident_id() -> str:
    """
    Generate a unique incident identifier.
    
    Format: inc_{timestamp}_{random}
    
    Returns:
        Unique incident ID string
    """
    timestamp = int(datetime.utcnow().timestamp())
    random_part = uuid.uuid4().hex[:6]
    return f"inc_{timestamp}_{random_part}"

