# Testing Guide - Trauma Detection System

## 🚀 Quick Start Testing

### Step 1: Configure Your Phone Numbers and Emails

**Option A: Use the setup script (Recommended)**
```powershell
cd backend\src
python setup_test_env.py
```

**Option B: Create .env file manually**
```powershell
cd backend\src
# Create .env file with your details
```

Add these to `.env`:
```env
FAMILY_PHONE=+919876543210          # Your WhatsApp number
FAMILY_EMAIL=your.email@gmail.com    # Your email
HOSPITAL_PHONE=+919876543211         # Teammate's phone (hospital)
HOSPITAL_EMAIL=teammate@gmail.com    # Teammate's email (hospital)
```

### Step 2: Start the Server

```powershell
cd backend\src
python app.py
```

Or with uvicorn:
```powershell
cd backend\src
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`

### Step 3: Run the Test

**Option A: Use the test script (Easiest)**
```powershell
cd backend\src
python test_crash.py
```

**Option B: Use curl/Postman**

```bash
curl -X POST http://localhost:8000/api/trigger/crash \
  -H "Content-Type: application/json" \
  -d '{
    "g_force": 5.2,
    "heart_rate": 145.0,
    "heart_rate_after": 45.0,
    "voice_decibels": 0.0,
    "gps": {
      "lat": 19.0760,
      "lon": 72.8777
    },
    "blood_type": "O+",
    "allergies": ["Penicillin"],
    "user_consent": true
  }'
```

## 📱 What Happens During Testing

1. **Phase 1 (0-10 seconds)**: Triangulation
   - System checks: G-Force > 4G ✅
   - Heart rate spike > 140 BPM then drop < 50 BPM ✅
   - No voice response ✅
   - **Result**: CRITICAL_EVENT_CONFIRMED

2. **Phase 2 (10-30 seconds)**: Multi-Agent Swarm
   - **Agent A (Dispatcher)**: 
     - Finds nearest hospital
     - Calls `HOSPITAL_PHONE` (your teammate) with emergency alert
   - **Agent B (Guardian)**:
     - Generates medical QR code
     - Creates first responder dashboard
   - **Agent C (Treasurer)**:
     - Generates pre-auth token (₹50,000)
     - Emails token to `HOSPITAL_EMAIL` (teammate's email)

3. **Phase 3 (When user arrives at hospital)**:
   - Sends notification to `FAMILY_PHONE` and `FAMILY_EMAIL` (your number/email)

## 📧 What You'll Receive

### On Your Teammate's Phone (HOSPITAL_PHONE):
- **Emergency Call/SMS** from dispatcher
- Message: "Automated Alert. Severe Crash at [location]. User Unresponsive. Blood Type O+. Dispatch ACLS unit."

### On Your Teammate's Email (HOSPITAL_EMAIL):
- **Pre-Authorization Email** with:
  - Pre-auth token (e.g., PREAUTH_20241201_ABC123)
  - Authorized amount: ₹50,000
  - Patient medical information

### On Your Phone/Email (FAMILY_PHONE/FAMILY_EMAIL):
- **Arrival Notification** (when Phase 3 triggers)
- Message: "User has arrived at City Hospital. Vitals are stable. Ward number pending."

## 🔧 Configuration Files

- **`.env`**: Environment variables (phone numbers, emails, API keys)
- **`test_crash.py`**: Test script with configurable values
- **`setup_test_env.py`**: Interactive setup script

## ⚠️ Important Notes

1. **Phone Format**: Must be in E.164 format (e.g., `+919876543210`)
2. **Mock Mode**: System works without Twilio/SendGrid API keys (uses mock calls/emails)
3. **Real Calls**: For actual phone calls, you need Twilio credentials
4. **Real Emails**: For actual emails, you need SMTP or SendGrid credentials

## 🐛 Troubleshooting

**Server won't start:**
- Check if port 8000 is available
- Make sure all dependencies are installed: `pip install -r requirements.txt`

**No notifications received:**
- Check `.env` file has correct phone numbers/emails
- Check server logs for errors
- In mock mode, notifications are printed to console

**Import errors:**
- Make sure you're in `backend/src` directory
- Check Python path includes `backend/src`

## 📊 Expected Output

When you run the test, you should see:
```
🚨 CRASH DETECTION TRIGGERED 🚨
[PHASE 1] Running triangulation...
[PHASE 1] CRITICAL_EVENT_CONFIRMED
[PHASE 2] Activating Multi-Agent Swarm...
[AGENT A - DISPATCHER] Finding nearest trauma center...
[AGENT B - GUARDIAN] Generating First Responder Dashboard...
[AGENT C - TREASURER] Generating pre-auth token...
✅ SUCCESS!
```

Check your phone and email for notifications!

