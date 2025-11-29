"""
Quick script to check if Twilio credentials are loaded correctly
"""

from config.settings import settings

print("="*70)
print("TWILIO CONFIGURATION CHECK")
print("="*70)
print(f"TWILIO_ACCOUNT_SID: {'[OK] Set' if settings.TWILIO_ACCOUNT_SID else '[X] Not Set'}")
if settings.TWILIO_ACCOUNT_SID:
    print(f"  Value: {settings.TWILIO_ACCOUNT_SID[:10]}...{settings.TWILIO_ACCOUNT_SID[-5:]}")
print(f"TWILIO_AUTH_TOKEN: {'[OK] Set' if settings.TWILIO_AUTH_TOKEN else '[X] Not Set'}")
if settings.TWILIO_AUTH_TOKEN:
    print(f"  Value: {settings.TWILIO_AUTH_TOKEN[:10]}...{settings.TWILIO_AUTH_TOKEN[-5:]}")
print(f"TWILIO_PHONE_NUMBER: {'[OK] Set' if settings.TWILIO_PHONE_NUMBER else '[X] Not Set'}")
if settings.TWILIO_PHONE_NUMBER:
    print(f"  Value: {settings.TWILIO_PHONE_NUMBER}")
print(f"FAMILY_PHONE: {'[OK] Set' if settings.FAMILY_PHONE else '[X] Not Set'}")
if settings.FAMILY_PHONE:
    print(f"  Value: {settings.FAMILY_PHONE}")
print("="*70)

if settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN and settings.TWILIO_PHONE_NUMBER:
    print("[OK] All Twilio credentials are configured!")
    print("   Real calls and SMS will be sent.")
else:
    print("[!] Some Twilio credentials are missing!")
    print("   Mock calls and SMS will be used.")
print("="*70)

