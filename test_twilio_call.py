"""
Test script to verify Twilio call auto-play functionality
"""

import asyncio
import sys
import os

# Add backend/src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend', 'src'))

from agents.tools.twilio_service import make_call
from config.settings import settings
from utils.logger import logger


async def test_call():
    """Test Twilio call with auto-play message"""
    
    print("="*70)
    print("TESTING TWILIO CALL AUTO-PLAY")
    print("="*70)
    
    # Check if Twilio is configured
    if not settings.TWILIO_ACCOUNT_SID or not settings.TWILIO_AUTH_TOKEN:
        print("ERROR: Twilio credentials not configured!")
        print("   Add TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER to .env")
        return
    
    if not settings.FAMILY_PHONE:
        print("ERROR: FAMILY_PHONE not configured!")
        return
    
    test_message = (
        "Test message. This is an automated emergency alert. "
        "If you hear this message immediately after the trial verification, "
        "the auto-play feature is working correctly."
    )
    
    print(f"\nMaking test call to: {settings.FAMILY_PHONE}")
    print(f"Message: {test_message}")
    print("\nCalling...\n")
    
    try:
        result = await make_call(settings.FAMILY_PHONE, test_message)
        
        if result.get("success") or result.get("call_id"):
            print("="*70)
            print("CALL INITIATED SUCCESSFULLY")
            print("="*70)
            print(f"Call ID: {result.get('call_id', 'N/A')}")
            print(f"Status: {result.get('status', 'N/A')}")
            print("\nAnswer your phone and verify:")
            print("   1. Trial verification plays (Twilio requirement)")
            print("   2. Your message plays IMMEDIATELY after (no keypress needed)")
            print("="*70)
        else:
            print("ERROR: Call failed - check logs above")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(test_call())

