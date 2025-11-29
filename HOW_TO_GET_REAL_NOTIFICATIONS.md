# How to Get Real Phone Calls, SMS, and Emails

## Current Status: Mock Mode

Right now, the system is running in **mock mode** - calls and emails are simulated and printed to the **server console**, not actually sent.

## 📧 Option 1: Set Up Real Emails (EASIEST - Recommended)

### Gmail SMTP Setup (Free)

1. **Get Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in with your Gmail account
   - Select "Mail" and "Other (Custom name)"
   - Name it "Trauma System"
   - Copy the 16-character password

2. **Run the setup script:**
   ```powershell
   cd backend\src
   python setup_email.py
   ```

3. **Or manually add to `.env` file:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your.email@gmail.com
   SMTP_PASSWORD=your_16_char_app_password
   ```

4. **Restart the server:**
   ```powershell
   python app.py
   ```

Now emails will be sent for real! ✅

---

## 📞 Option 2: Set Up Real Phone Calls/SMS (Twilio - Paid)

### Twilio Setup

1. **Sign up for Twilio:**
   - Go to: https://www.twilio.com/try-twilio
   - Create a free account (includes $15.50 credit)

2. **Get your credentials:**
   - Account SID
   - Auth Token
   - Phone Number (provided by Twilio)

3. **Add to `.env` file:**
   ```env
   TWILIO_ACCOUNT_SID=your_account_sid
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

4. **Restart the server**

Now phone calls and SMS will be sent for real! ✅

---

## 🔍 Where to See Mock Output

If you're in mock mode, check the **SERVER TERMINAL** (where you ran `python app.py`). You'll see output like:

```
📞 [MOCK CALL] Emergency Call Simulated
To: +918454030044
Message: Automated Alert. Severe Crash at...
```

```
📧 [MOCK EMAIL] Pre-Authorization Email Simulated
To: vishal23borana@gmail.com
Pre-Auth Token: PREAUTH_20251127_ABC123
```

---

## 🎯 Quick Test After Setup

1. **For Email:** Run `python setup_email.py` and restart server
2. **For Phone:** Add Twilio credentials to `.env` and restart server
3. **Run test:** `python test_crash.py`
4. **Check your inbox/phone!**

---

## 💡 Recommendation

**Start with Email setup** (it's free and easier):
- Takes 2 minutes
- No credit card needed
- Works immediately
- You'll see real emails in your inbox

Then optionally add Twilio for phone calls/SMS if needed for your demo.

