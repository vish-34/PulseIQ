# Test Crash Simulation with curl

## 🚀 curl Commands

### **Option 1: Test with ngrok URL**

Replace `YOUR_NGROK_URL` with your actual ngrok URL:

```bash
curl -X GET "https://YOUR_NGROK_URL/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

**Example:**
```bash
curl -X GET "https://6b2418a8108c.ngrok-free.app/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

---

### **Option 2: Test Locally (localhost)**

If testing on the same machine where the server is running:

```bash
curl -X GET "http://localhost:8000/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

---

### **Option 3: Pretty Print JSON Response**

To see formatted JSON output:

```bash
curl -X GET "https://YOUR_NGROK_URL/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json" \
  | python -m json.tool
```

**Or on Windows PowerShell:**
```powershell
curl -X GET "https://YOUR_NGROK_URL/api/trigger/crash" `
  -H "X-Trigger-Token: CRASH_BUTTON" `
  -H "Content-Type: application/json" | ConvertFrom-Json | ConvertTo-Json -Depth 10
```

---

## ⚠️ Important Notes

1. **Header is REQUIRED**: Without `X-Trigger-Token: CRASH_BUTTON`, you'll get:
   ```json
   {
     "detail": "This endpoint requires X-Trigger-Token: CRASH_BUTTON header. Use from frontend button only."
   }
   ```

2. **Response**: On success, you'll get JSON with:
   - `incident_id`: Unique incident identifier
   - `status`: Current status
   - `gps`: GPS coordinates
   - `nearest_hospital`: Hospital information
   - `ambulance_dispatched`: Boolean
   - `insurance_preauth_token`: Pre-authorization token
   - `family_notified`: Boolean
   - `timestamp`: When it was triggered

---

## 🧪 Test Scenarios

### **Test 1: Without Header (Should Fail)**
```bash
curl -X GET "http://localhost:8000/api/trigger/crash"
```

**Expected:** 403 Forbidden error

### **Test 2: With Header (Should Work)**
```bash
curl -X GET "http://localhost:8000/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON"
```

**Expected:** JSON response with incident details, crash simulation starts

---

## 📝 Quick Copy-Paste (Windows PowerShell)

**Option 1: One-liner**
```powershell
Invoke-RestMethod -Uri "https://YOUR_NGROK_URL/api/trigger/crash" -Method GET -Headers @{"X-Trigger-Token"="CRASH_BUTTON"; "Content-Type"="application/json"}
```

**Option 2: Multi-line (easier to read)**
```powershell
$url = "https://YOUR_NGROK_URL/api/trigger/crash"
$headers = @{
    "X-Trigger-Token" = "CRASH_BUTTON"
    "Content-Type" = "application/json"
}
Invoke-RestMethod -Uri $url -Method GET -Headers $headers
```

**Option 3: Use the script file**
```powershell
.\TEST_CRASH_POWERSHELL.ps1
```

**⚠️ Note:** In PowerShell, `curl` is an alias for `Invoke-WebRequest` which has different syntax. Use `Invoke-RestMethod` instead!

---

## 📝 Quick Copy-Paste (Linux/Mac)

```bash
# Replace YOUR_NGROK_URL with your actual ngrok URL
curl -X GET "https://YOUR_NGROK_URL/api/trigger/crash" \
  -H "X-Trigger-Token: CRASH_BUTTON" \
  -H "Content-Type: application/json"
```

