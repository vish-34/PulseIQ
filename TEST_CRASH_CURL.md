# Test Crash Simulation with curl

## 🚀 Quick Test Commands

### **Option 1: Test with ngrok URL**

Replace `YOUR_NGROK_URL` with your actual ngrok URL:

```bash
curl -X GET "https://YOUR_NGROK_URL/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

**Example with actual ngrok URL:**
```bash
curl -X GET "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

---

### **Option 2: Test Locally (localhost)**

If testing on the same machine where the server is running:

```bash
curl -X GET "http://localhost:5000/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

---

### **Option 3: Windows PowerShell**

**One-liner:**
```powershell
Invoke-RestMethod -Uri "https://YOUR_NGROK_URL/api/trigger/crash" -Method GET -Headers @{"X-Trigger-Token"="CRASH_BUTTON"; "Content-Type"="application/json"}
```

**With your ngrok URL:**
```powershell
Invoke-RestMethod -Uri "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash" -Method GET -Headers @{"X-Trigger-Token"="CRASH_BUTTON"; "Content-Type"="application/json"}
```

**Multi-line (easier to read):**
```powershell
$url = "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash"
$headers = @{
    "X-Trigger-Token" = "CRASH_BUTTON"
    "Content-Type" = "application/json"
}
Invoke-RestMethod -Uri $url -Method GET -Headers $headers
```

---

## ✅ What to Expect

### **In Your Backend Terminal:**

You should see:
```
======================================================================
🔔 INCOMING REQUEST DETECTED!
======================================================================
Method: GET
Path: /api/trigger/crash
X-Trigger-Token: CRASH_BUTTON
======================================================================
======================================================================
GET /api/trigger/crash - Crash button pressed from frontend (valid token)
...
======================================================================
🚨 CRASH DETECTION TRIGGERED 🚨
======================================================================
```

Then the crash simulation will start!

### **In curl Response:**

You'll get JSON with:
```json
{
  "incident_id": "INC_20241215_123456_ABC123",
  "status": "PROTOCOL_ACTIVE",
  "gps": {
    "lat": 19.168,
    "lon": 72.85
  },
  "nearest_hospital": {...},
  "ambulance_dispatched": true,
  "insurance_preauth_token": "PREAUTH_...",
  "family_notified": true,
  "timestamp": "..."
}
```

---

## ⚠️ Important Notes

1. **Header is REQUIRED**: Without `X-Trigger-Token: CRASH_BUTTON`, you'll get 403 Forbidden
2. **Takes ~35 seconds**: The crash simulation takes time (5s consciousness test + 30s transport)
3. **Watch your terminal**: All logs will appear in your backend terminal

---

## 🧪 Test Scenarios

### **Test 1: Without Header (Should Fail)**
```bash
curl -X GET "http://localhost:5000/api/trigger/crash"
```

**Expected:** 403 Forbidden error

### **Test 2: With Header (Should Work)**
```bash
curl -X GET "http://localhost:5000/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON"
```

**Expected:** JSON response, crash simulation starts

---

## 📝 Quick Copy-Paste

**For ngrok (replace URL):**
```bash
curl -X GET "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash" -H "X-Trigger-Token: CRASH_BUTTON" -H "Content-Type: application/json"
```

**For localhost:**
```bash
curl -X GET "http://localhost:5000/api/trigger/crash" -H "X-Trigger-Token: CRASH_BUTTON" -H "Content-Type: application/json"
```

**PowerShell:**
```powershell
Invoke-RestMethod -Uri "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash" -Method GET -Headers @{"X-Trigger-Token"="CRASH_BUTTON"; "Content-Type"="application/json"}
```

