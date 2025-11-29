"""
Direct Email Test - Tests if emails are actually being sent

This script directly tests the email sending functionality to verify SMTP is working.
"""

import asyncio
import sys
import os

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from config.settings import settings
from agents.tools.email_service import send_preauth_email, send_family_notification


async def test_email_sending():
    """Test email sending directly"""
    print("="*70)
    print("📧 TESTING EMAIL SENDING")
    print("="*70)
    print(f"\nSMTP Configuration:")
    print(f"  Host: {settings.SMTP_HOST}")
    print(f"  Port: {settings.SMTP_PORT}")
    print(f"  User: {settings.SMTP_USER}")
    print(f"  Password: {'*' * len(settings.SMTP_PASSWORD) if settings.SMTP_PASSWORD else 'NOT SET'}")
    print(f"\nTarget Emails:")
    print(f"  Hospital: {settings.HOSPITAL_EMAIL}")
    print(f"  Family: {settings.FAMILY_EMAIL}")
    print("="*70 + "\n")
    
    # Check if SMTP is configured
    if not settings.SMTP_HOST or not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print("❌ ERROR: SMTP not fully configured!")
        print("\nRequired settings:")
        print("  SMTP_HOST=smtp.gmail.com")
        print("  SMTP_PORT=587")
        print("  SMTP_USER=your.email@gmail.com")
        print("  SMTP_PASSWORD=your_app_password")
        return False
    
    # Test 1: Send pre-auth email to hospital
    print("📤 Test 1: Sending pre-auth email to hospital...")
    print(f"   To: {settings.HOSPITAL_EMAIL}")
    
    try:
        result1 = await send_preauth_email(
            hospital_email=settings.HOSPITAL_EMAIL,
            token="TEST_TOKEN_12345",
            user_info={
                "name": "Test Patient",
                "blood_type": "O+",
                "allergies": ["Penicillin"],
                "emergency_contact": "+917738187807"
            },
            amount=50000.0,
            incident_id="TEST_INCIDENT_001"
        )
        
        if result1:
            print("   ✅ Email sent successfully!")
        else:
            print("   ❌ Email failed to send")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        result1 = False
    
    print("\n" + "-"*70 + "\n")
    
    # Test 2: Send family notification
    print("📤 Test 2: Sending family notification email...")
    print(f"   To: {settings.FAMILY_EMAIL}")
    
    try:
        result2 = await send_family_notification(
            family_email=settings.FAMILY_EMAIL,
            incident_info={
                "incident_id": "TEST_INCIDENT_001",
                "hospital_name": "City Trauma Center",
                "hospital_address": "123 Emergency Lane",
                "status": "stable"
            }
        )
        
        if result2:
            print("   ✅ Email sent successfully!")
        else:
            print("   ❌ Email failed to send")
    except Exception as e:
        print(f"   ❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        result2 = False
    
    print("\n" + "="*70)
    if result1 and result2:
        print("✅ ALL EMAILS SENT SUCCESSFULLY!")
        print(f"\n📧 Check these inboxes:")
        print(f"   - {settings.HOSPITAL_EMAIL}")
        print(f"   - {settings.FAMILY_EMAIL}")
    else:
        print("❌ SOME EMAILS FAILED")
        print("\nCheck the error messages above for details.")
    print("="*70 + "\n")
    
    return result1 and result2


if __name__ == "__main__":
    asyncio.run(test_email_sending())

