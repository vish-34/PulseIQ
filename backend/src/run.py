"""
Simple Run Script - Starts server in wait mode

Just run: python run.py
Server will wait for frontend button click.
"""

import subprocess
import sys

if __name__ == "__main__":
    print("="*70)
    print("TRAUMA DETECTION SYSTEM - SERVER MODE")
    print("="*70)
    print("\nStarting server - waiting for frontend requests...")
    print("Use ngrok to expose: ngrok http 5000")
    print("Frontend button should call: GET /api/trigger/crash")
    print("All output will appear in this terminal.\n")
    print("="*70 + "\n")
    
    # Run app.py WITHOUT --auto-test flag (server waits for requests)
    subprocess.run([sys.executable, "app.py"])

