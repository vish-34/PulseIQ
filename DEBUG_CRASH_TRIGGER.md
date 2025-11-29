# Debug Crash Trigger Issue

## 🚨 Problem
Friend's frontend shows "Crash triggered" but backend doesn't start simulation.

## ✅ Enhanced Logging Added

### **1. Request Logging**
- Now logs when request is received
- Shows client IP address
- Logs before and after processing

### **2. Error Logging**
- Full traceback on errors
- Clear error messages
- Step-by-step logging

### **3. Success Logging**
- Confirms when simulation starts
- Shows incident ID
- Clear success messages

---

## 🔍 How to Debug

### **Step 1: Check Backend Logs**
When friend clicks button, you should see:
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

### **Step 2: Check for Errors**
If you see error messages, they'll show:
- What went wrong
- Full traceback
- Where it failed

### **Step 3: Verify ngrok Connection**
Make sure:
- Backend is running on port 5000
- ngrok is forwarding to port 5000
- Friend is using correct ngrok URL

---

## 🧪 Test Steps

1. **Start Backend:**
   ```powershell
   python run.py
   ```

2. **Start ngrok:**
   ```powershell
   ngrok http 5000
   ```

3. **Check Backend Logs:**
   - Watch terminal for log messages
   - Should see request received
   - Should see crash simulation starting

4. **Friend Clicks Button:**
   - Frontend sends request
   - Backend should log immediately
   - Simulation should start

---

## ⚠️ Common Issues

### **Issue 1: No Logs Appear**
- **Cause**: Request not reaching backend
- **Fix**: Check ngrok URL, check port 5000

### **Issue 2: Error in Logs**
- **Cause**: Exception in crash handler
- **Fix**: Check error message, fix the issue

### **Issue 3: Request Received but No Simulation**
- **Cause**: Error in handle_crash_trigger
- **Fix**: Check traceback in logs

---

## 📝 Next Steps

1. **Restart backend** with new logging
2. **Have friend click button again**
3. **Check backend terminal** for logs
4. **Share logs** if issue persists

