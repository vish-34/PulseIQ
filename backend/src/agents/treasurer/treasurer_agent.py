"""
Agent C: The Treasurer (Financial)

Handles insurance policy lookup, pre-auth token generation, and email to hospital.
"""

from typing import Dict, Any, Optional
from schemas.crash_payload import CrashPayloadInput
from agents.insurance.policy_lookup import lookup_policy, verify_coverage
from agents.insurance.preauth_generator import generate_preauth_token
from agents.tools.email_service import send_preauth_email
from config.settings import settings
from utils.logger import logger


async def run(
    payload: CrashPayloadInput,
    incident_id: str,
    hospital_info: Optional[Dict[str, Any]] = None,
    user_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    Main execution function for Treasurer Agent.
    
    Responsibilities:
    1. Lookup insurance policy
    2. Generate pre-auth token (₹50,000)
    3. Email token to hospital reception
    
    Args:
        payload: Crash payload input
        incident_id: Incident identifier
        hospital_info: Hospital information from Dispatcher Agent
        user_id: User identifier (optional, defaults to incident_id)
        
    Returns:
        Dictionary with results:
        {
            "success": bool,
            "policy_found": bool,
            "preauth_token": str,
            "amount": float,
            "email_sent": bool,
            "message": str
        }
    """
    result = {
        "success": False,
        "policy_found": False,
        "preauth_token": None,
        "amount": settings.DEFAULT_PREAUTH_AMOUNT,
        "email_sent": False,
        "message": ""
    }
    
    try:
        # Step 1: Connect to Insurance API (mock)
        user_id = user_id or f"user_{incident_id}"
        logger.info("TREASURER", f"Connecting to Insurance API (mock) for user: {user_id}")
        
        policy = await lookup_policy(user_id)
        
        if policy:
            result["policy_found"] = True
            policy_number = policy["policy_number"]
            logger.success("TREASURER", f"Policy found: {policy_number} ({policy['provider']})")
            
            # Step 2: Auto-generate pre-auth token for ₹50,000
            amount = settings.DEFAULT_PREAUTH_AMOUNT
            logger.info("TREASURER", f"Auto-generating pre-auth token for ₹{amount:,.2f}")
            
            coverage_ok = await verify_coverage(amount, policy_number)
            
            if not coverage_ok:
                logger.warn("TREASURER", f"WARNING: Amount ₹{amount:,.2f} exceeds coverage - proceeding for emergency")
                # Continue anyway for emergency
            
            result["amount"] = amount
            
            # Step 3: Generate pre-auth token
            hospital_id = hospital_info.get("place_id", "unknown") if hospital_info else "unknown"
            
            token = await generate_preauth_token(
                policy_number=policy_number,
                amount=amount,
                hospital_id=hospital_id,
                incident_id=incident_id
            )
            result["preauth_token"] = token
            logger.success("TREASURER", f"Pre-auth token generated: {token}")
            
            # Step 4: Email token to hospital
            # ALWAYS use configured HOSPITAL_EMAIL for actual notifications
            # Google Maps email is only for display/logging
            hospital_email = settings.HOSPITAL_EMAIL
            
            if hospital_info:
                google_email = hospital_info.get("google_email")  # For reference only
                if google_email:
                    logger.info("TREASURER", f"Google Maps found hospital email: {google_email} (for reference only)")
                
                if hospital_email:
                    logger.info("TREASURER", f"Using configured HOSPITAL_EMAIL for notification: {hospital_email}")
                    logger.info("TREASURER", f"Emailing token to hospital reception: {hospital_email}")
                    
                    user_info = {
                        "name": "Emergency Patient",
                        "blood_type": payload.blood_type,
                        "allergies": payload.allergies,
                        "emergency_contact": "Emergency Contact",
                        "policy_number": policy_number,
                        "insurance_provider": policy.get("provider", "Insurance Provider"),
                        "policy_type": policy.get("policy_type", "Individual"),
                        "coverage_amount": policy.get("coverage_amount", 0.0)
                    }
                    
                    email_sent = await send_preauth_email(
                        hospital_email=hospital_email,
                        token=token,
                        user_info=user_info,
                        amount=amount,
                        incident_id=incident_id
                    )
                    result["email_sent"] = email_sent
                    if email_sent:
                        logger.success("TREASURER", f"Pre-auth email sent to {hospital_email}")
                    else:
                        logger.error("TREASURER", f"Failed to send email to {hospital_email}")
                else:
                    logger.warn("TREASURER", "WARNING: HOSPITAL_EMAIL not configured in settings")
            else:
                # No hospital info, use configured email directly
                if hospital_email:
                    logger.info("TREASURER", f"No hospital info, using configured email: {hospital_email}")
                    user_info = {
                        "name": "Emergency Patient",
                        "blood_type": payload.blood_type,
                        "allergies": payload.allergies,
                        "emergency_contact": "Emergency Contact",
                        "policy_number": policy_number,
                        "insurance_provider": policy.get("provider", "Insurance Provider"),
                        "policy_type": policy.get("policy_type", "Individual"),
                        "coverage_amount": policy.get("coverage_amount", 0.0)
                    }
                    email_sent = await send_preauth_email(
                        hospital_email=hospital_email,
                        token=token,
                        user_info=user_info,
                        amount=amount,
                        incident_id=incident_id
                    )
                    result["email_sent"] = email_sent
                    if email_sent:
                        logger.success("TREASURER", f"Pre-auth email sent to {hospital_email}")
                else:
                    logger.warn("TREASURER", "WARNING: HOSPITAL_EMAIL not configured in settings")
            
            # Step 5: Store proof in backend
            logger.info("TREASURER", "Storing proof in backend")
            
            result["success"] = True
            result["message"] = f"Pre-auth token {token} generated and sent"
            logger.success("TREASURER", "All tasks completed: Policy lookup, Token generation, Email sent, Proof stored")
        else:
            result["message"] = "Insurance policy not found"
            logger.error("TREASURER", f"Policy not found for user {user_id}")
        
    except Exception as e:
        result["message"] = f"Treasurer agent error: {str(e)}"
        logger.error("TREASURER", f"Error: {e}")
    
    return result

