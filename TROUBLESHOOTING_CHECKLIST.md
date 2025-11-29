# Troubleshooting Checklist - Crash Simulation Not Starting

## 🔍 Step-by-Step Diagnostic Process

### **Step 1: Verify Backend is Running**

**Check:**
```powershell
# Look at your backend terminal
# Should see:
Server running at: http://0.0.0.0:5000
WAITING FOR FRONTEND BUTTON CLICK...
```

**✅ If you see this:** Backend is running  
**❌ If not:** Start backend with `python run.py`

---

### **Step 2: Verify ngrok is Running**

**Check:**
```powershell
# Look at ngrok terminal
# Should see:
Forwarding    https://abc123.ngrok-free.app -> http://localhost:5000
```

**✅ If you see this:** ngrok is forwarding to port 5000  
**❌ If not:** Start ngrok with `ngrok http 5000`

**⚠️ IMPORTANT:** Port must be **5000** (not 8000 or any other port)

---

### **Step 3: Test Basic Connection**

**Have your friend test this URL in browser:**
```
https://YOUR_NGROK_URL/api/test
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Backend is reachable!",
  "timestamp": "...",
  "client_ip": "...",
  "user_agent": "..."
}
```

**✅ If you see this:** Connection is working!  
**❌ If error:** ngrok URL is wrong or backend not running

**Check your backend terminal:** Should see log: `Test endpoint called from: [IP]`

---

### **Step 4: Test Crash Endpoint (Without Triggering)**

**Have your friend test this URL in browser:**
```
https://YOUR_NGROK_URL/api/test/crash-endpoint
```

**Expected Response:**
```json
{
  "status": "success",
  "message": "Crash endpoint test - connection working!",
  "headers_received": {
    "x-trigger-token": "NOT PROVIDED",
    "has_valid_token": false
  }
}
```

**✅ If you see this:** Endpoint is reachable  
**Check your backend terminal:** Should see log about the test

---

### **Step 5: Verify Frontend Code**

**Your friend's code should be:**
```javascript
const triggerCrash = async () => {
  const friendURL = "https://YOUR_NGROK_URL/api/trigger/crash";
  try {
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "X-Trigger-Token": "CRASH_BUTTON"  // ← MUST HAVE THIS
      }
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    const data = await res.json();
    console.log("Crash triggered:", data);
    alert("Crash triggered! Incident ID: " + data.incident_id);
    
  } catch (err) {
    console.error("Error:", err);
    alert("⚠ Error: " + err.message);
  }
};
```

**Check:**
- ✅ URL is correct (includes `/api/trigger/crash`)
- ✅ Method is `GET`
- ✅ Header `X-Trigger-Token: CRASH_BUTTON` is included
- ✅ Error handling shows actual error message

---

### **Step 6: Check Backend Logs When Button is Clicked**

**When friend clicks button, you should see in backend terminal:**

```
======================================================================
GET /api/trigger/crash - Crash button pressed from frontend (valid token)
Request received from: [IP_ADDRESS]
======================================================================
Creating crash payload and starting simulation...
Calling handle_crash_trigger()...
======================================================================
🚨 CRASH DETECTION TRIGGERED 🚨
======================================================================
```

**✅ If you see this:** Request is reaching backend, simulation should start  
**❌ If you see nothing:** Request is not reaching backend

---

### **Step 7: Check for Errors**

**If you see error messages in backend terminal:**
- Read the error message carefully
- Check the traceback
- Common errors:
  - Missing dependencies
  - Configuration errors
  - Import errors

---

## 🚨 Common Issues & Fixes

### **Issue 1: No Logs Appear When Button is Clicked**

**Possible Causes:**
1. Wrong ngrok URL
2. Port mismatch (ngrok forwarding to wrong port)
3. CORS blocking request
4. Request not being sent

**Fix:**
1. Verify ngrok URL is correct
2. Check ngrok shows `-> http://localhost:5000`
3. Check backend is on port 5000
4. Test with `/api/test` endpoint first

---

### **Issue 2: 403 Forbidden Error**

**Cause:** Missing or wrong `X-Trigger-Token` header

**Fix:**
- Ensure frontend includes: `"X-Trigger-Token": "CRASH_BUTTON"`
- Check browser console for actual headers sent

---

### **Issue 3: CORS Error in Browser Console**

**Cause:** CORS not configured correctly

**Fix:**
- Backend already allows all origins (`"*"`)
- If still error, check ngrok URL is correct

---

### **Issue 4: Request Reaches Backend But No Simulation**

**Possible Causes:**
1. Exception in `handle_crash_trigger`
2. Error in crash detection logic
3. Missing configuration

**Fix:**
- Check backend logs for error messages
- Look for traceback
- Verify all environment variables are set

---

## ✅ Verification Checklist

Before testing, ensure:

- [ ] Backend is running on port 5000
- [ ] ngrok is forwarding to port 5000
- [ ] ngrok URL is correct (no typos)
- [ ] Frontend code includes `X-Trigger-Token: CRASH_BUTTON` header
- [ ] Frontend URL ends with `/api/trigger/crash`
- [ ] Backend terminal is visible to see logs
- [ ] Test endpoint `/api/test` works first

---

## 🧪 Testing Order

1. **Test 1:** `/api/test` - Verify basic connection
2. **Test 2:** `/api/test/crash-endpoint` - Verify endpoint reachable
3. **Test 3:** Click crash button - Should trigger simulation

If Test 1 fails → Connection issue  
If Test 1 works but Test 2 fails → Endpoint issue  
If Test 2 works but Test 3 fails → Header or crash logic issue

---

## 📝 What to Share for Help

If still not working, share:

1. **Backend terminal output** (when button is clicked)
2. **ngrok terminal output** (showing forwarding)
3. **Frontend code** (the triggerCrash function)
4. **Browser console errors** (if any)
5. **Response from `/api/test` endpoint**

This will help identify exactly where the issue is!

