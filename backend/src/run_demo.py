"""
Demo Runner - Runs the server with automatic test

This script starts the server and automatically triggers a crash detection test.
Everything happens in one terminal - no need for separate terminals!
"""

import subprocess
import sys
import os

def main():
    """Run the server with auto-test enabled"""
    print("="*70)
    print("🚀 TRAUMA DETECTION SYSTEM - DEMO MODE")
    print("="*70)
    print("\nThis will:")
    print("  1. Start the server")
    print("  2. Automatically trigger a crash detection test")
    print("  3. Show all results in this terminal")
    print("\n📱 Make sure your phone numbers and emails are configured in .env")
    print("="*70 + "\n")
    
    # Set auto-test environment variable
    os.environ["AUTO_TEST"] = "1"
    
    # Run the app with auto-test flag
    try:
        subprocess.run([sys.executable, "app.py", "--auto-test"], check=True)
    except KeyboardInterrupt:
        print("\n\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()

