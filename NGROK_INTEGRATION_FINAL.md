# ngrok Integration - Final Setup

## ✅ System Status

- ✅ **Server waits** - No auto-trigger code
- ✅ **GET endpoint ready** - `/api/trigger/crash`
- ✅ **CORS configured** - Allows all origins
- ✅ **Ready for ngrok** - Server accepts external connections

---

## 🚀 Step-by-Step Process

### **Step 1: Start Your Server**
```powershell
cd C:\Users\Shayesta Shaikh\MHCC
python run.py
```

**Expected Output:**
```
Trauma Detection System Started
Server running at: http://0.0.0.0:8000
API Docs at: http://0.0.0.0:8000/docs

WAITING FOR FRONTEND BUTTON CLICK...
  - Frontend button: GET /api/trigger/crash
  - Custom payload: POST /api/trigger/crash

Server is ready. Crash simulation will ONLY start when button is clicked.
```

**✅ Server is now WAITING - No crash simulation yet!**

---

### **Step 2: Start ngrok (In NEW Terminal)**
```powershell
ngrok http 8000
```

**⚠️ IMPORTANT:** The port number `8000` MUST match your backend port!

**Expected Output:**
```
Forwarding    https://6b2418a8108c.ngrok-free.app -> http://localhost:8000
                                                      ^^^^^^
                                                      Port 8000 (matches backend)
```

**Copy the URL:** `https://6b2418a8108c.ngrok-free.app`

**✅ Verification:** Check that ngrok shows `-> http://localhost:8000` (same port as backend)

---

### **Step 3: Give URL to Your Friend**

**Give them the complete URL:**
```
https://6b2418a8108c.ngrok-free.app/api/trigger/crash
```

**Important:** Make sure the URL ends with `/api/trigger/crash` (not duplicated!)

---

### **Step 4: Friend Updates Frontend Code**

**Your friend's code is almost correct, just update the URL:**

```javascript
const triggerCrash = async () => {
  // Update this URL with your ngrok URL
  const friendURL = "https://6b2418a8108c.ngrok-free.app/api/trigger/crash";
  
  try {
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    const data = await res.json();
    console.log("Crash triggered:", data);
    alert("Crash triggered on remote device! Incident ID: " + data.incident_id);
    
  } catch (err) {
    console.error("Error:", err);
    alert("⚠ Unable to reach crash system: " + err.message);
  }
};
```

---

### **Step 5: Friend Clicks Button**

**When button is clicked:**
1. Frontend sends GET request to ngrok URL
2. ngrok forwards to your server (`localhost:8000`)
3. Server receives request at `/api/trigger/crash`
4. **ONLY THEN** crash simulation starts
5. Full emergency response protocol executes

---

## ✅ Guaranteed Flow

1. ✅ **You start server** → `python run.py` → Server waits
2. ✅ **You start ngrok** → `ngrok http 8000` → Get public URL
3. ✅ **You give URL** → Friend gets: `https://...ngrok-free.app/api/trigger/crash`
4. ✅ **Friend updates code** → Uses your ngrok URL
5. ✅ **Friend clicks button** → GET request sent
6. ✅ **Server receives request** → Crash simulation starts
7. ✅ **Full system executes** → All phases run

---

## 🔍 Verification

### **Test 1: Server is Waiting**
After `python run.py`, you should see:
- ✅ "WAITING FOR FRONTEND BUTTON CLICK..."
- ✅ No crash simulation logs
- ✅ Server just waiting

### **Test 2: ngrok is Working**
After `ngrok http 8000`, you should see:
- ✅ "Forwarding https://...ngrok-free.app -> http://localhost:8000"
- ✅ Web interface at http://127.0.0.1:4040

### **Test 3: Endpoint is Accessible**
From browser, visit:
```
https://YOUR_NGROK_URL/api/trigger/crash
```

You should see JSON response (crash simulation will start!)

---

## ⚠️ Important Notes

1. **Server must be running FIRST** before starting ngrok
2. **ngrok URL changes** each time you restart ngrok (unless you have paid plan)
3. **Update friend's code** with new URL if ngrok restarts
4. **Keep both terminals open**:
   - Terminal 1: `python run.py` (server)
   - Terminal 2: `ngrok http 8000` (tunnel)

---

## 📝 Summary

- ✅ **Server waits** until button is clicked
- ✅ **ngrok exposes** your server to internet
- ✅ **Friend connects** via ngrok URL
- ✅ **Button click** triggers crash simulation
- ✅ **All features intact** - Full emergency response

**The system is ready! Follow the steps above and it will work perfectly.**

