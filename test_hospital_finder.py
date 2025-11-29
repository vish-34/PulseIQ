"""
Test script to verify Google Maps API finds nearest hospital to NESCO Centre Goregaon
"""

import asyncio
import sys
import os
from pathlib import Path

# Change to backend/src directory to load .env correctly
backend_src = Path(__file__).parent / 'backend' / 'src'
os.chdir(backend_src)
sys.path.insert(0, str(backend_src))

from agents.tools.maps_service import find_nearest_trauma_center
from schemas.crash_payload import GPSLocation
from config.settings import settings
from utils.logger import logger


async def test_hospital_finder():
    """Test finding nearest hospital to NESCO Centre Goregaon"""
    
    print("="*70)
    print("TESTING HOSPITAL FINDER - NESCO Centre Goregaon")
    print("="*70)
    
    # Check if API key is configured
    if not settings.GOOGLE_MAPS_API_KEY:
        print("ERROR: GOOGLE_MAPS_API_KEY not configured!")
        print("   Add your API key to backend/src/.env file")
        print("   See GOOGLE_MAPS_API_SETUP.md for instructions")
        return
    
    print(f"API Key configured: {settings.GOOGLE_MAPS_API_KEY[:20]}...")
    print()
    
    # NESCO Centre Goregaon coordinates
    nesco_location = GPSLocation(lat=19.1680, lon=72.8500)
    
    print(f"Crash Location: NESCO Centre Goregaon")
    print(f"GPS Coordinates: {nesco_location.lat}, {nesco_location.lon}")
    print()
    print("Searching for nearest hospital...")
    print()
    
    try:
        hospital = await find_nearest_trauma_center(nesco_location)
        
        print("="*70)
        print("HOSPITAL FOUND")
        print("="*70)
        print(f"Hospital Name: {hospital.get('name', 'Unknown')}")
        print(f"Address: {hospital.get('address', 'Unknown')}")
        print(f"Distance: {hospital.get('distance_km', 0):.2f} km")
        print(f"GPS: {hospital.get('gps', {}).get('lat', 0)}, {hospital.get('gps', {}).get('lon', 0)}")
        print()
        print("Phone/Email (for reference):")
        print(f"  Phone: {hospital.get('phone', 'Not available')}")
        print(f"  Email: {hospital.get('email', 'Not available')}")
        print()
        print("Note: Actual notifications will use your configured:")
        print(f"  HOSPITAL_PHONE: {settings.HOSPITAL_PHONE}")
        print(f"  HOSPITAL_EMAIL: {settings.HOSPITAL_EMAIL}")
        print("="*70)
        
        if hospital.get('name') and hospital.get('name') != 'Unknown Hospital':
            print()
            print("SUCCESS: Nearest hospital found!")
            print("The system will use this hospital for the emergency response.")
        else:
            print()
            print("WARNING: Hospital name not found. Check API key and permissions.")
            
    except Exception as e:
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
        print()
        print("Troubleshooting:")
        print("1. Check if GOOGLE_MAPS_API_KEY is correct in .env")
        print("2. Verify Places API is enabled in Google Cloud Console")
        print("3. Check if billing is enabled (required even for free tier)")


if __name__ == "__main__":
    asyncio.run(test_hospital_finder())

