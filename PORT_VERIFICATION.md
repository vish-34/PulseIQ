# Port Verification - Backend & ngrok

## ✅ Current Configuration

### **Backend Server Port: 8000**
- **File**: `backend/src/app.py` (line 92)
- **Code**: `uvicorn.run(app, host="0.0.0.0", port=8000)`
- **Status**: ✅ Fixed at port 8000

### **ngrok Forwarding: 8000**
- **Command**: `ngrok http 8000`
- **Status**: ✅ Must forward to port 8000

---

## 🚀 Correct Setup Process

### **Step 1: Start Backend (Port 8000)**
```powershell
python run.py
```

**Expected Output:**
```
Server running at: http://0.0.0.0:8000
```

**✅ Backend is now running on port 8000**

---

### **Step 2: Start ngrok (Forward to Port 8000)**
```powershell
ngrok http 8000
```

**Expected Output:**
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
```

**✅ ngrok is forwarding to port 8000 (same as backend)**

---

## ✅ Verification Checklist

- [ ] Backend shows: `Server running at: http://0.0.0.0:8000`
- [ ] ngrok shows: `-> http://localhost:8000`
- [ ] Both are using port **8000**

---

## 🔍 How to Verify Ports Match

### **Check Backend Port:**
Look at the server startup message:
```
Server running at: http://0.0.0.0:8000
```

### **Check ngrok Port:**
Look at ngrok output:
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:8000
                                                      ^^^^^^
                                                      Port 8000
```

---

## ⚠️ Common Mistakes

### **❌ Wrong ngrok Command:**
```powershell
ngrok http 3000  # ❌ Wrong! Backend is on 8000, not 3000
```

### **✅ Correct ngrok Command:**
```powershell
ngrok http 8000  # ✅ Correct! Matches backend port
```

---

## 📝 Summary

- **Backend Port**: Always **8000** (hardcoded in `app.py`)
- **ngrok Command**: Always `ngrok http 8000`
- **They MUST match**: Both use port 8000

**If you see different ports, something is wrong!**

