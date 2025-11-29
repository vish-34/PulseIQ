"""
Policy Lookup - Insurance Policy Verification

Looks up user insurance policies and verifies coverage.
"""

from typing import Dict, Any, Optional
import random


# Mock insurance database with randomized providers
INSURANCE_PROVIDERS = [
    "HealthCare Insurance Ltd",
    "MediCover Insurance",
    "Star Health Insurance",
    "HDFC ERGO Health Insurance",
    "ICICI Lombard Health Insurance",
    "Bajaj Allianz Health Insurance",
    "Reliance Health Insurance",
    "Aditya Birla Health Insurance",
    "Future Generali Health Insurance",
    "ManipalCigna Health Insurance",
    "Care Health Insurance",
    "Niva Bupa Health Insurance"
]

# Mock insurance database (in production, this would be a real database/API)
MOCK_POLICIES = {
    "user_001": {
        "policy_number": "POL-2024-001234",
        "provider": "HealthCare Insurance Ltd",
        "coverage_amount": 500000.0,  # ₹5,00,000
        "active": True,
        "user_id": "user_001"
    },
    "user_002": {
        "policy_number": "POL-2024-005678",
        "provider": "MediCover Insurance",
        "coverage_amount": 1000000.0,  # ₹10,00,000
        "active": True,
        "user_id": "user_002"
    }
}


async def lookup_policy(user_id: str) -> Optional[Dict[str, Any]]:
    """
    Look up insurance policy for a user.
    
    Args:
        user_id: User identifier
        
    Returns:
        Dictionary containing policy information:
        {
            "policy_number": str,
            "provider": str,
            "coverage_amount": float,
            "active": bool,
            "user_id": str
        }
        Returns None if no policy found
    """
    # Check mock database
    policy = MOCK_POLICIES.get(user_id)
    
    if policy:
        return policy.copy()
    
    # In production, this would query a real database or API
    # For demo, return a randomized policy if user not found
    # This ensures different details each time
    provider = random.choice(INSURANCE_PROVIDERS)
    policy_number = f"POL-2024-{random.randint(100000, 999999)}"
    # Random coverage between ₹3,00,000 and ₹15,00,000
    coverage_amount = random.uniform(300000.0, 1500000.0)
    
    return {
        "policy_number": policy_number,
        "provider": provider,
        "coverage_amount": round(coverage_amount, 2),
        "active": True,
        "user_id": user_id,
        "policy_type": random.choice(["Individual", "Family", "Group"]),
        "valid_until": "2025-12-31"  # Mock expiry date
    }


async def verify_coverage(amount: float, policy_number: str) -> bool:
    """
    Verify if the requested amount is within policy coverage.
    
    Args:
        amount: Amount to verify (₹)
        policy_number: Insurance policy number
        
    Returns:
        True if amount is within coverage, False otherwise
    """
    # Find policy by policy number
    for user_id, policy in MOCK_POLICIES.items():
        if policy["policy_number"] == policy_number:
            return policy["active"] and amount <= policy["coverage_amount"]
    
    # Default: assume coverage if policy exists
    return True


async def get_policy_by_number(policy_number: str) -> Optional[Dict[str, Any]]:
    """
    Get policy information by policy number.
    
    Args:
        policy_number: Insurance policy number
        
    Returns:
        Policy dictionary or None if not found
    """
    for user_id, policy in MOCK_POLICIES.items():
        if policy["policy_number"] == policy_number:
            return policy.copy()
    
    return None

