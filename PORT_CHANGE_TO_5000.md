# Port Changed to 5000

## ✅ Changes Made

### **1. Backend Server Port: 5000**
- **File**: `backend/src/app.py`
- **Changed**: `uvicorn.run(app, host="0.0.0.0", port=5000)`
- **Status**: ✅ Updated

### **2. Startup Messages: 5000**
- **File**: `backend/src/app.py`
- **Changed**: All port references updated to 5000
- **Status**: ✅ Updated

### **3. Run Scripts: 5000**
- **File**: `run.py` and `backend/src/run.py`
- **Changed**: ngrok command updated to `ngrok http 5000`
- **Status**: ✅ Updated

---

## 🚀 Updated Commands

### **Start Backend:**
```powershell
python run.py
```

**Expected Output:**
```
Server running at: http://0.0.0.0:5000
```

### **Start ngrok:**
```powershell
ngrok http 5000
```

**Expected Output:**
```
Forwarding    https://abc123.ngrok-free.app -> http://localhost:5000
```

---

## ⚠️ Important Notes

1. **Port Changed**: From 8000 → 5000
2. **ngrok Command**: Now use `ngrok http 5000` (not 8000)
3. **Frontend URL**: Update to use port 5000 if testing locally
4. **All Features**: Remain intact, only port changed

---

## 📝 Summary

- ✅ **Backend Port**: 5000
- ✅ **ngrok Command**: `ngrok http 5000`
- ✅ **Both Match**: Port 5000

**Note**: FastAPI uses `uvicorn.run()`, not `app.run()`. The syntax is correct for FastAPI.

