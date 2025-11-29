# Send Real Emails to Your Configured Addresses

## ✅ Your Current Configuration

- **Hospital Email**: vishal23borana@gmail.com (will receive pre-auth token)
- **Family Email**: rookiedev.mujahid@gmail.com (will receive notifications)
- **Hospital Phone**: +918454030044 (will receive calls/SMS)
- **Family Phone**: +917738187807 (will receive SMS)

## 🚀 Quick Setup - Send Real Emails (2 minutes)

### Step 1: Get Gmail App Password

1. Go to: **https://myaccount.google.com/apppasswords**
2. Sign in with **any Gmail account** (can be different from the recipient emails)
3. Click "Select app" → "Mail"
4. Click "Select device" → "Other (Custom name)"
5. Type: `Trauma System`
6. Click "Generate"
7. **Copy the 16-character password** (remove spaces)

### Step 2: Add to .env File

Open `backend/src/.env` and add these lines:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.gmail@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

**Example:**
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=myemail@gmail.com
SMTP_PASSWORD=abcd efgh ijkl mnop
```

### Step 3: Restart Server

```powershell
# Stop server (Ctrl+C in server terminal)
# Then restart:
cd backend\src
python app.py
```

### Step 4: Test

```powershell
python test_crash.py
```

## ✅ Result

Emails will be sent to:
- ✅ **vishal23borana@gmail.com** - Pre-auth token email
- ✅ **rookiedev.mujahid@gmail.com** - Family notification email

## 📞 For Real Phone Calls/SMS

You need Twilio (paid, but has free trial):

1. Sign up: https://www.twilio.com/try-twilio (free $15.50 credit)
2. Get credentials from dashboard
3. Add to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```
4. Restart server

Calls/SMS will go to:
- ✅ **+918454030044** - Emergency dispatcher call
- ✅ **+917738187807** - Family SMS notification

## 🎯 Summary

- ✅ Phone numbers and emails are **already configured correctly**
- ⚠️ Need **SMTP credentials** for real emails (Gmail is free)
- ⚠️ Need **Twilio credentials** for real calls/SMS (paid, but free trial available)

The system will use your configured numbers/emails once you add the credentials!

