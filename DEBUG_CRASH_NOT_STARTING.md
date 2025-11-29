# Debug: Crash Simulation Not Starting

## 🚨 Problem
Frontend gets success response, but crash simulation doesn't start in backend terminal.

## ✅ Enhanced Logging Added

### **1. Request Entry Logging**
- Logs when request is received
- Shows payload values being used
- Confirms function is being called

### **2. Triangulation Logging**
- Shows payload values (G-Force, HR, Voice)
- Logs triangulation result
- Warns if triangulation fails (early return)

### **3. Function Completion Logging**
- Logs when `handle_crash_trigger()` is called
- Logs when it completes
- Shows incident ID and status

---

## 🔍 What to Check

### **Step 1: Check if Request is Reaching Backend**

When friend clicks button, you should IMMEDIATELY see:
```
======================================================================
GET /api/trigger/crash - Crash button pressed from frontend (valid token)
Request received from: [IP]
======================================================================
Creating crash payload and starting simulation...
Payload: G-Force=5.2, HR=145.0, HR_after=45.0, Voice=0.0
======================================================================
CALLING handle_crash_trigger() NOW...
This will take ~35 seconds (5s consciousness test + 30s transport)
======================================================================
```

**✅ If you see this:** Request is reaching backend  
**❌ If you see nothing:** Request not reaching backend (check ngrok/port)

---

### **Step 2: Check if Triangulation is Passing**

You should see:
```
======================================================================
Running triangulation - Checking 3 confirmations:
Payload values: G-Force=5.2, HR=145.0, HR_after=45.0, Voice=0.0
Triangulation completed: is_critical=True, status=CRITICAL_EVENT_CONFIRMED
✅ All 3 confirmations met - Proceeding with crash simulation
```

**✅ If you see this:** Triangulation passed, simulation should continue  
**❌ If you see "NOT CRITICAL":** Triangulation failed, function returns early

---

### **Step 3: Check if Crash Simulation Starts**

You should see:
```
======================================================================
🚨 CRASH DETECTION TRIGGERED 🚨
======================================================================
Incident ID: INC_YYYYMMDD_HHMMSS_XXXXXX
Starting crash detection and emergency response protocol...
```

**✅ If you see this:** Crash simulation is starting  
**❌ If you don't see this:** Function is returning before this point

---

## 🚨 Common Issues

### **Issue 1: No Logs at All**

**Possible Causes:**
- Request not reaching backend
- Wrong ngrok URL
- Port mismatch
- CORS blocking

**Fix:**
1. Test `/api/test` endpoint first
2. Check ngrok is forwarding to port 5000
3. Check backend is on port 5000
4. Verify ngrok URL is correct

---

### **Issue 2: Logs Stop After "CALLING handle_crash_trigger()"**

**Possible Causes:**
- Exception in `handle_crash_trigger`
- Import error
- Configuration error
- Silent exception

**Fix:**
- Check for error messages in logs
- Look for traceback
- Check all environment variables are set

---

### **Issue 3: "NOT CRITICAL" Message**

**Possible Causes:**
- Triangulation failing (payload values wrong)
- G-Force not > 4.0
- Heart rate not meeting criteria
- Voice decibels not 0.0

**Fix:**
- Check payload values in logs
- Verify default payload is correct
- Check triangulation logic

---

### **Issue 4: Function Returns But No Simulation**

**Possible Causes:**
- Early return in triangulation
- Exception caught silently
- Function completing too fast

**Fix:**
- Check for "NOT CRITICAL" message
- Check for error messages
- Verify all async operations are awaited

---

## 📝 Next Steps

1. **Restart backend** with new logging
2. **Have friend click button**
3. **Watch backend terminal carefully**
4. **Share the logs** you see (or don't see)

The enhanced logging will show exactly where it's failing!

