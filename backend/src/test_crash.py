"""
Test Script for Crash Detection System

This script allows you to test the trauma detection system with real phone numbers and emails.

Usage:
1. Update the phone numbers and emails in this file
2. Make sure the server is running: python app.py
3. Run this script: python test_crash.py
"""

import requests
import json
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Fix Windows console encoding for emojis
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Load environment variables from .env file
load_dotenv()

# ============================================
# CONFIGURATION - UPDATE THESE VALUES
# ============================================

# Your phone number (for family notifications via WhatsApp/SMS)
# Can be set in .env file as FAMILY_PHONE
FAMILY_PHONE = os.getenv("FAMILY_PHONE", "+917738187807")  # YOUR WhatsApp number

# Your teammate's phone number (for hospital/dispatcher)
# Can be set in .env file as HOSPITAL_PHONE
HOSPITAL_PHONE = os.getenv("HOSPITAL_PHONE", "+918454030044")  # TEAMMATE's phone (hospital)

# Your email (for family notifications)
# Can be set in .env file as FAMILY_EMAIL
FAMILY_EMAIL = os.getenv("FAMILY_EMAIL", "rookiedev.mujahid@gmail.com")  # YOUR email

# Hospital/Teammate email (for pre-auth token)
# Can be set in .env file as HOSPITAL_EMAIL
HOSPITAL_EMAIL = os.getenv("HOSPITAL_EMAIL", "vishal23borana@gmail.com")  # TEAMMATE's email (hospital)

# Test location (Mumbai coordinates - change if needed)
TEST_LAT = 19.0760
TEST_LON = 72.8777

# API endpoint
API_URL = "http://localhost:8000/api/trigger/crash"


def create_test_payload():
    """Create a test crash payload"""
    return {
        "g_force": 5.2,  # High impact (>4G threshold)
        "heart_rate": 145.0,  # Spike (>140 BPM)
        "heart_rate_after": 45.0,  # Drop (<50 BPM - unconscious)
        "voice_decibels": 0.0,  # No voice response
        "gps": {
            "lat": TEST_LAT,
            "lon": TEST_LON
        },
        "blood_type": "O+",
        "allergies": ["Penicillin"],
        "user_consent": True
    }


def test_crash_detection():
    """Test the crash detection endpoint"""
    print("="*70)
    print("🚨 TESTING CRASH DETECTION SYSTEM 🚨")
    print("="*70)
    print(f"\n📡 API Endpoint: {API_URL}")
    print(f"📱 Family Phone: {FAMILY_PHONE}")
    print(f"🏥 Hospital Phone: {HOSPITAL_PHONE}")
    print(f"📧 Family Email: {FAMILY_EMAIL}")
    print(f"📧 Hospital Email: {HOSPITAL_EMAIL}")
    print("\n" + "="*70 + "\n")
    
    # Check if configuration is updated (skip warning if real numbers are set)
    if "+919876543210" in FAMILY_PHONE or "+919876543211" in HOSPITAL_PHONE:
        print("⚠️  WARNING: Using default test numbers!")
        print("\nTo use your real numbers, either:")
        print("  1. Update values in test_crash.py")
        print("  2. Create .env file with FAMILY_PHONE, HOSPITAL_PHONE, etc.")
        print("\nPhone numbers must be in E.164 format (e.g., +919876543210)")
        response = input("\nContinue with test numbers? (y/n): ")
        if response.lower() != 'y':
            print("Exiting...")
            return
    
    payload = create_test_payload()
    
    print("📤 Sending crash detection request...")
    print(f"\nPayload:\n{json.dumps(payload, indent=2)}\n")
    
    try:
        print("⏳ Waiting for response (this may take 30-40 seconds)...\n")
        response = requests.post(API_URL, json=payload, timeout=60)
        
        print("="*70)
        print("📥 RESPONSE:")
        print("="*70)
        print(f"Status Code: {response.status_code}\n")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ SUCCESS!")
            print(f"\n📋 Incident ID: {result.get('incident_id')}")
            print(f"📊 Status: {result.get('status')}")
            print(f"🚑 Ambulance Dispatched: {result.get('ambulance_dispatched')}")
            print(f"💰 Pre-Auth Token: {result.get('insurance_preauth_token')}")
            
            if result.get('nearest_hospital'):
                hospital = result['nearest_hospital']
                print(f"\n🏥 Hospital: {hospital.get('name')}")
                print(f"📍 Distance: {hospital.get('distance_km')} km")
                print(f"📞 Hospital Phone: {hospital.get('phone')}")
                print(f"📧 Hospital Email: {hospital.get('email')}")
            
            print("\n" + "="*70)
            print("📱 CHECK YOUR PHONE AND EMAIL FOR NOTIFICATIONS!")
            print("="*70)
            print(f"\nYou should receive:")
            print(f"  ✅ SMS/Call on {HOSPITAL_PHONE} (from dispatcher)")
            print(f"  ✅ Email on {HOSPITAL_EMAIL} (pre-auth token)")
            print(f"  ✅ SMS/Email on {FAMILY_PHONE}/{FAMILY_EMAIL} (arrival notification)")
            print("="*70)
        else:
            print(f"❌ ERROR: {response.status_code}")
            print(response.text)
            
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to API")
        print("\nMake sure the server is running:")
        print("  cd backend/src")
        print("  python app.py")
        print("\nOr with uvicorn:")
        print("  uvicorn app:app --reload --host 0.0.0.0 --port 8000")
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_crash_detection()
