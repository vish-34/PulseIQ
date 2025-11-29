"""
Email Service - Pre-Auth Tokens and Notifications

Sends pre-authorization emails to hospitals and notifications to families.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any, Optional
from config.settings import settings


async def send_preauth_email(
    hospital_email: str,
    token: str,
    user_info: Dict[str, Any],
    amount: float,
    incident_id: str
) -> bool:
    """
    Send pre-authorization token email to hospital reception.
    
    Args:
        hospital_email: Hospital email address
        token: Pre-authorization token
        user_info: User information dictionary
        amount: Pre-authorized amount (₹)
        incident_id: Incident identifier
        
    Returns:
        True if email sent successfully, False otherwise
    """
    # Try to send real email first, fallback to mock if no credentials
    # Check if SMTP is configured - if yes, send real email
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        # SMTP is configured - send real email
        try:
            subject = f"Emergency Pre-Authorization - Incident {incident_id}"
            
            # Get insurance details from user_info if available
            policy_number = user_info.get('policy_number', 'N/A')
            insurance_provider = user_info.get('insurance_provider', 'Insurance Provider')
            policy_type = user_info.get('policy_type', 'Individual')
            
            # Email body template with hospital admission fee details
            body = f"""
Emergency Medical Pre-Authorization & Hospital Admission

═══════════════════════════════════════════════════════════
INCIDENT DETAILS
═══════════════════════════════════════════════════════════
Incident ID: {incident_id}
Pre-Authorization Token: {token}
Authorized Amount: ₹{amount:,.2f}

═══════════════════════════════════════════════════════════
HOSPITAL ADMISSION FEE
═══════════════════════════════════════════════════════════
Hospital Admission Fee: ₹50,000.00
This amount is pre-authorized and ready for immediate processing.

═══════════════════════════════════════════════════════════
PATIENT INFORMATION
═══════════════════════════════════════════════════════════
- Name: {user_info.get('name', 'Unknown')}
- Blood Type: {user_info.get('blood_type', 'Unknown')}
- Allergies: {', '.join(user_info.get('allergies', [])) or 'None'}
- Emergency Contact: {user_info.get('emergency_contact', 'Not provided')}

═══════════════════════════════════════════════════════════
INSURANCE INFORMATION
═══════════════════════════════════════════════════════════
- Insurance Provider: {insurance_provider}
- Policy Number: {policy_number}
- Policy Type: {policy_type}
- Coverage Status: Active

═══════════════════════════════════════════════════════════
AUTHORIZATION DETAILS
═══════════════════════════════════════════════════════════
This pre-authorization token authorizes:
- Immediate hospital admission
- Medical treatment up to ₹{amount:,.2f}
- Hospital admission fee: ₹50,000.00 (included in authorized amount)

Token Validity: 24 hours from issuance
Token Status: Active and ready for use

Please proceed with patient admission and use this token for billing authorization.

For billing inquiries, please reference:
- Pre-Auth Token: {token}
- Incident ID: {incident_id}

---
Automated Emergency Response System
Emergency Financial Pre-Authorization Service
            """.strip()
            
            if settings.SENDGRID_API_KEY:
                return await _send_via_sendgrid(hospital_email, subject, body)
            else:
                return await _send_via_smtp(hospital_email, subject, body)
        except Exception as e:
            print(f"Email send error: {e}")
            return False
    
    # No SMTP configured - mock mode
    print("\n" + "="*70)
    print("📧 [MOCK EMAIL] Pre-Authorization Email Simulated")
    print("="*70)
    print(f"To: {hospital_email}")
    print(f"Subject: Emergency Pre-Authorization - Incident {incident_id}")
    print(f"Pre-Auth Token: {token}")
    print(f"Authorized Amount: ₹{amount:,.2f}")
    print(f"Hospital Admission Fee: ₹50,000.00")
    print(f"Patient: {user_info.get('name', 'Unknown')}")
    print(f"Blood Type: {user_info.get('blood_type', 'Unknown')}")
    print(f"Insurance Provider: {user_info.get('insurance_provider', 'N/A')}")
    print(f"Policy Number: {user_info.get('policy_number', 'N/A')}")
    print("="*70 + "\n")
    print("⚠️  NOTE: This is a MOCK email. Add SMTP credentials to .env for real emails")
    print("="*70 + "\n")
    return True
    
    try:
        subject = f"Emergency Pre-Authorization - Incident {incident_id}"
        
        # Email body template
        body = f"""
Emergency Medical Pre-Authorization

Incident ID: {incident_id}
Pre-Authorization Token: {token}
Authorized Amount: ₹{amount:,.2f}

Patient Information:
- Name: {user_info.get('name', 'Unknown')}
- Blood Type: {user_info.get('blood_type', 'Unknown')}
- Allergies: {', '.join(user_info.get('allergies', [])) or 'None'}
- Emergency Contact: {user_info.get('emergency_contact', 'Not provided')}

This token authorizes immediate medical treatment up to ₹{amount:,.2f}.
Token is valid for 24 hours from issuance.

Please admit the patient and use this token for billing authorization.

---
Automated Emergency Response System
        """.strip()
        
        if settings.SENDGRID_API_KEY:
            return await _send_via_sendgrid(hospital_email, subject, body)
        else:
            return await _send_via_smtp(hospital_email, subject, body)
            
    except Exception as e:
        print(f"Email send error: {e}")
        return False


async def send_family_notification(
    family_email: str,
    incident_info: Dict[str, Any]
) -> bool:
    """
    Send notification to family about incident status.
    
    Args:
        family_email: Family/emergency contact email
        incident_info: Incident information dictionary
        
    Returns:
        True if email sent successfully, False otherwise
    """
    # Check if SMTP is configured - if yes, send real email
    if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:
        # SMTP is configured - send real email
        try:
            hospital_name = incident_info.get("hospital_name", "City Hospital")
            status = incident_info.get("status", "stable")
            incident_id = incident_info.get("incident_id", "Unknown")
            hospital_address = incident_info.get("hospital_address", "Location not available")
            message = incident_info.get("message", "")
            
            # Determine email type based on status
            if status == "crash_detected_emergency_dispatched":
                # Crash alert email
                subject = f"🚨 EMERGENCY ALERT - Crash Detected - {incident_id}"
                body = f"""
🚨 EMERGENCY ALERT - Crash Detected

A crash has been detected and emergency services are being dispatched immediately.

INCIDENT DETAILS:
- Incident ID: {incident_id}
- Location: {hospital_address}
- Status: Emergency services dispatched
- Message: {message}

Emergency responders are on their way. We will keep you updated as more information becomes available.

---
Automated Emergency Response System
                """.strip()
            else:
                # Hospital arrival email
                subject = f"Emergency Update - {incident_id}"
                body = f"""
Emergency Update

Your family member has arrived at {hospital_name}.
Current status: {status.replace('_', ' ').title()}.
Ward number: Pending assignment.

Incident ID: {incident_id}
Location: {hospital_address}

{message if message else "We will keep you updated as more information becomes available."}

---
Automated Emergency Response System
                """.strip()
            
            if settings.SENDGRID_API_KEY:
                return await _send_via_sendgrid(family_email, subject, body)
            else:
                return await _send_via_smtp(family_email, subject, body)
        except Exception as e:
            print(f"Email send error: {e}")
            return False
    
    # No SMTP configured - mock mode
    print("\n" + "="*70)
    print("📧 [MOCK EMAIL] Family Notification Email Simulated")
    print("="*70)
    print(f"To: {family_email}")
    print(f"Subject: Emergency Update - {incident_info.get('incident_id', 'Incident')}")
    print(f"Hospital: {incident_info.get('hospital_name', 'City Hospital')}")
    print(f"Status: {incident_info.get('status', 'stable')}")
    print("="*70 + "\n")
    print("⚠️  NOTE: This is a MOCK email. Add SMTP credentials to .env for real emails")
    print("="*70 + "\n")
    return True
    
    try:
        hospital_name = incident_info.get("hospital_name", "City Hospital")
        status = incident_info.get("status", "stable")
        
        subject = f"Emergency Update - {incident_info.get('incident_id', 'Incident')}"
        
        body = f"""
Emergency Update

Your family member has arrived at {hospital_name}.
Current status: Vitals are {status}.
Ward number: Pending assignment.

Incident ID: {incident_info.get('incident_id', 'Unknown')}
Location: {incident_info.get('hospital_address', 'Hospital')}

We will keep you updated as more information becomes available.

---
Automated Emergency Response System
        """.strip()
        
        if settings.SENDGRID_API_KEY:
            return await _send_via_sendgrid(family_email, subject, body)
        else:
            return await _send_via_smtp(family_email, subject, body)
            
    except Exception as e:
        print(f"Email send error: {e}")
        return False


async def _send_via_smtp(to_email: str, subject: str, body: str) -> bool:
    """Send email via SMTP"""
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.SMTP_USER
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(msg)
        
        print(f"\n✅ [REAL EMAIL] Successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False


async def _send_via_smtp_auto(to_email: str, subject: str, body: str, smtp_user: str, smtp_password: str) -> bool:
    """Send email via SMTP with auto-detected Gmail settings"""
    try:
        msg = MIMEMultipart()
        msg['From'] = smtp_user
        msg['To'] = to_email
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(smtp_user, smtp_password)
            server.send_message(msg)
        
        print(f"\n✅ [REAL EMAIL] Successfully sent to {to_email}")
        return True
    except Exception as e:
        print(f"SMTP error: {e}")
        return False


async def _send_via_sendgrid(to_email: str, subject: str, body: str) -> bool:
    """Send email via SendGrid API"""
    try:
        import httpx
        
        async with httpx.AsyncClient() as client:
            url = "https://api.sendgrid.com/v3/mail/send"
            headers = {
                "Authorization": f"Bearer {settings.SENDGRID_API_KEY}",
                "Content-Type": "application/json"
            }
            data = {
                "personalizations": [{"to": [{"email": to_email}]}],
                "from": {"email": settings.SMTP_USER or "noreply@trauma-system.com"},
                "subject": subject,
                "content": [{"type": "text/plain", "value": body}]
            }
            
            response = await client.post(url, json=data, headers=headers, timeout=10.0)
            response.raise_for_status()
            return True
    except Exception as e:
        print(f"SendGrid error: {e}")
        return False

