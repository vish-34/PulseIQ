"""
Quick Email Setup for Real Email Notifications

This script helps you set up Gmail SMTP for real email notifications.
"""

import os

def setup_gmail_smtp():
    """Interactive setup for Gmail SMTP"""
    print("="*70)
    print("📧 GMAIL SMTP SETUP FOR REAL EMAIL NOTIFICATIONS")
    print("="*70)
    print("\nTo send REAL emails, you need:")
    print("1. Gmail account")
    print("2. App Password (not your regular password)")
    print("\nSteps to get App Password:")
    print("  1. Go to: https://myaccount.google.com/apppasswords")
    print("  2. Select 'Mail' and 'Other (Custom name)'")
    print("  3. Name it 'Trauma System'")
    print("  4. Copy the 16-character password")
    print("\n" + "="*70 + "\n")
    
    email = input("Enter your Gmail address: ").strip()
    app_password = input("Enter your Gmail App Password (16 characters): ").strip()
    
    if not email or not app_password:
        print("❌ Email and password are required!")
        return
    
    # Read existing .env file
    env_file = ".env"
    env_content = ""
    
    if os.path.exists(env_file):
        with open(env_file, "r") as f:
            env_content = f.read()
    
    # Update or add SMTP settings
    lines = env_content.split("\n")
    updated_lines = []
    smtp_added = False
    
    for line in lines:
        if line.startswith("SMTP_HOST="):
            updated_lines.append("SMTP_HOST=smtp.gmail.com")
            smtp_added = True
        elif line.startswith("SMTP_USER="):
            updated_lines.append(f"SMTP_USER={email}")
            smtp_added = True
        elif line.startswith("SMTP_PASSWORD="):
            updated_lines.append(f"SMTP_PASSWORD={app_password}")
            smtp_added = True
        elif line.startswith("SMTP_PORT="):
            updated_lines.append("SMTP_PORT=587")
            smtp_added = True
        else:
            updated_lines.append(line)
    
    # Add SMTP settings if not found
    if not smtp_added:
        updated_lines.append("")
        updated_lines.append("# Gmail SMTP Configuration")
        updated_lines.append("SMTP_HOST=smtp.gmail.com")
        updated_lines.append("SMTP_PORT=587")
        updated_lines.append(f"SMTP_USER={email}")
        updated_lines.append(f"SMTP_PASSWORD={app_password}")
    
    # Write back to .env
    with open(env_file, "w") as f:
        f.write("\n".join(updated_lines))
    
    print(f"\n✅ Gmail SMTP configured in {env_file}")
    print("\n📋 Configuration:")
    print(f"  SMTP Host: smtp.gmail.com")
    print(f"  SMTP Port: 587")
    print(f"  Email: {email}")
    print(f"  Password: {'*' * len(app_password)}")
    print("\n🚀 Restart the server for changes to take effect!")
    print("="*70)


if __name__ == "__main__":
    setup_gmail_smtp()

