"""
Simple Run Script - Starts server with automatic test

Run from project root: python run.py
Everything happens automatically in one terminal!
"""

import subprocess
import sys
import os

if __name__ == "__main__":
    # Change to backend/src directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    backend_src = os.path.join(script_dir, "backend", "src")
    
    if not os.path.exists(backend_src):
        print("❌ ERROR: backend/src directory not found!")
        print(f"   Looking for: {backend_src}")
        sys.exit(1)
    
    print("="*70)
    print("TRAUMA DETECTION SYSTEM - SERVER MODE")
    print("="*70)
    print("\nStarting server - waiting for frontend requests...")
    print("Use ngrok to expose: ngrok http 5000")
    print("Frontend button should call: GET /api/trigger/crash")
    print("All output will appear in this terminal.\n")
    print("="*70 + "\n")
    
    # Change to backend/src and run app.py (no auto-test)
    os.chdir(backend_src)
    try:
        subprocess.run([sys.executable, "app.py"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

