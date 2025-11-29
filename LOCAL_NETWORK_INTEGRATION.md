# Local Network Integration Guide (No ngrok)

## 🎯 Setup for Two Laptops on Same Network

This guide shows how to connect your friend's frontend (his laptop) to your backend server (your laptop) without using ngrok.

---

## ✅ What You Need

1. **Both laptops on the same WiFi network** (or same local network)
2. **Your laptop**: Running the backend server
3. **Friend's laptop**: Running the frontend
4. **Your laptop's IP address** (to give to your friend)

---

## 📋 Step-by-Step Setup

### **Step 1: Find Your Laptop's IP Address**

#### **On Windows (Your Laptop):**
```powershell
ipconfig
```

Look for **"IPv4 Address"** under your WiFi adapter:
```
Wireless LAN adapter Wi-Fi:
   IPv4 Address. . . . . . . . . . . : 192.168.1.100
```

**Your IP will be something like:** `192.168.1.100` or `192.168.0.105`

#### **Alternative Method:**
```powershell
# Get just the IP address
ipconfig | findstr "IPv4"
```

---

### **Step 2: Update Backend Server to Accept Network Connections**

The server is already configured to accept connections from any IP (`0.0.0.0`), so it should work. But let's verify:

**File**: `backend/src/app.py` (Line 92)
```python
uvicorn.run(app, host="0.0.0.0", port=8000)  # ✅ Already correct!
```

**✅ Already configured correctly!** The `host="0.0.0.0"` means it accepts connections from any IP on your network.

---

### **Step 3: Configure Windows Firewall**

Windows Firewall might block incoming connections. You need to allow port 8000:

#### **Option A: Allow via PowerShell (Run as Administrator)**
```powershell
New-NetFirewallRule -DisplayName "Python FastAPI Server" -Direction Inbound -LocalPort 8000 -Protocol TCP -Action Allow
```

#### **Option B: Allow via Windows Settings**
1. Open **Windows Defender Firewall**
2. Click **"Advanced settings"**
3. Click **"Inbound Rules"** → **"New Rule"**
4. Select **"Port"** → **Next**
5. Select **"TCP"** → Enter port **8000** → **Next**
6. Select **"Allow the connection"** → **Next**
7. Check all profiles → **Next**
8. Name: **"Python FastAPI Server"** → **Finish**

---

### **Step 4: Start Your Server**

```powershell
cd C:\Users\Shayesta Shaikh\MHCC
python run.py
```

**You should see:**
```
Trauma Detection System Started
Server running at: http://0.0.0.0:8000
WAITING FOR FRONTEND BUTTON CLICK...
```

---

### **Step 5: Give Your Friend the Connection Details**

**Give your friend:**
- **Your IP Address**: `192.168.1.100` (use your actual IP from Step 1)
- **Port**: `8000`
- **Full URL**: `http://192.168.1.100:8000/api/trigger/crash`

**Example:**
```
Backend Server URL: http://192.168.1.100:8000/api/trigger/crash
```

---

### **Step 6: Friend Updates Frontend Code**

**Your friend should use this in his frontend:**

```javascript
const triggerCrash = async () => {
  // Replace 192.168.1.100 with YOUR actual IP address
  const friendURL = "http://192.168.1.100:8000/api/trigger/crash";
  
  try {
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "Content-Type": "application/json"
      }
    });
    
    if (!res.ok) {
      throw new Error("Crash system unreachable");
    }
    
    const data = await res.json();
    console.log("Crash triggered:", data);
    alert("Crash triggered! Incident ID: " + data.incident_id);
    
  } catch (err) {
    console.error("Error:", err);
    alert("⚠ Unable to reach crash system: " + err.message);
  }
};
```

---

## 🔧 Troubleshooting

### **Issue 1: "Connection refused" or "ERR_CONNECTION_REFUSED"**

**Causes:**
- Firewall blocking port 8000
- Server not running
- Wrong IP address

**Solutions:**
1. Check firewall (Step 3)
2. Verify server is running: `python run.py`
3. Verify IP address: `ipconfig`

---

### **Issue 2: "ERR_NETWORK_CHANGED" or Timeout**

**Causes:**
- Different WiFi networks
- IP address changed

**Solutions:**
1. Make sure both laptops on **same WiFi**
2. Get new IP address: `ipconfig`
3. Update friend's frontend with new IP

---

### **Issue 3: CORS Error**

**Solution:** Already fixed! The backend allows all origins (`"*"`), so CORS should work.

---

### **Issue 4: Can't Find IP Address**

**Try these commands:**
```powershell
# Method 1
ipconfig | findstr "IPv4"

# Method 2
Get-NetIPAddress -AddressFamily IPv4 | Where-Object {$_.InterfaceAlias -like "*Wi-Fi*"}

# Method 3 - Get all IPs
ipconfig /all
```

---

## 🧪 Testing Connection

### **Test 1: From Your Laptop**
```powershell
# Test if server is accessible
curl http://localhost:8000/health
```

### **Test 2: From Friend's Laptop**
```powershell
# Replace with your IP
curl http://192.168.1.100:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "Trauma Detection System",
  "version": "1.0.0"
}
```

---

## 📝 Quick Checklist

- [ ] Both laptops on same WiFi network
- [ ] Found your IP address (`ipconfig`)
- [ ] Configured Windows Firewall (allow port 8000)
- [ ] Server running (`python run.py`)
- [ ] Friend has your IP address
- [ ] Friend updated frontend code with your IP
- [ ] Tested connection from friend's laptop

---

## 🎯 Summary

1. **Your laptop**: 
   - Find IP: `ipconfig`
   - Allow firewall: Port 8000
   - Start server: `python run.py`

2. **Friend's laptop**:
   - Use your IP in frontend: `http://YOUR_IP:8000/api/trigger/crash`
   - Click button → Triggers crash simulation

3. **Both on same WiFi** → Connection works!

---

## ⚠️ Important Notes

- **IP changes**: If you disconnect/reconnect WiFi, your IP might change. Get new IP and update friend.
- **Same network required**: Both laptops must be on the same WiFi/network.
- **Firewall**: Must allow port 8000 for this to work.
- **No internet needed**: Works on local network only.

---

## 🔗 Alternative: If Not on Same Network

If you're on different networks, you have two options:

1. **Use ngrok** (what we set up earlier)
2. **Port forwarding** (complex, requires router access)
3. **VPN** (connect both to same VPN)

For hackathon, **same WiFi network** is easiest!

