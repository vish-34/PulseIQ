# Quick Email Setup - Send Real Emails NOW

## 🚀 Fast Setup (2 minutes)

### Step 1: Get Gmail App Password

1. Go to: **https://myaccount.google.com/apppasswords**
2. Sign in with your Gmail account
3. Click "Select app" → Choose "Mail"
4. Click "Select device" → Choose "Other (Custom name)"
5. Type: `Trauma System`
6. Click "Generate"
7. **Copy the 16-character password** (looks like: `abcd efgh ijkl mnop`)

### Step 2: Add to .env file

Open `backend/src/.env` and add:

```env
# Gmail SMTP (for real emails)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

**OR** use the setup script:
```powershell
cd backend\src
python setup_email.py
```

### Step 3: Restart Server

```powershell
# Stop current server (Ctrl+C)
# Then restart:
python app.py
```

### Step 4: Test Again

```powershell
python test_crash.py
```

## ✅ That's it!

Now emails will be sent to:
- **vishal23borana@gmail.com** (pre-auth token)
- **rookiedev.mujahid@gmail.com** (family notification)

## 📞 For Phone Calls/SMS

You'll need Twilio (paid service):
1. Sign up: https://www.twilio.com/try-twilio
2. Get Account SID, Auth Token, Phone Number
3. Add to `.env`:
   ```env
   TWILIO_ACCOUNT_SID=your_sid
   TWILIO_AUTH_TOKEN=your_token
   TWILIO_PHONE_NUMBER=+1234567890
   ```

## 🎯 Current Status

- ✅ **Phone numbers configured**: +917738187807, +918454030044
- ✅ **Emails configured**: rookiedev.mujahid@gmail.com, vishal23borana@gmail.com
- ⚠️ **Need SMTP credentials** for real emails
- ⚠️ **Need Twilio credentials** for real calls/SMS

