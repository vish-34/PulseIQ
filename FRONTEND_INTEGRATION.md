# Frontend Integration Guide

## ✅ Changes Made

### **1. Removed Auto-Test on Startup**
- **File**: `backend/src/app.py`
- **Change**: Server no longer auto-triggers crash simulation on startup
- **Result**: Server starts and waits for requests

### **2. Added GET Endpoint for Frontend Button**
- **File**: `backend/src/routes/trigger_routes.py`
- **New Endpoint**: `GET /api/trigger/crash`
- **Purpose**: Triggered when frontend "Crash Button" is pressed
- **Data**: Uses default test data (NESCO Centre Goregaon location)

### **3. Kept POST Endpoint for Custom Data**
- **File**: `backend/src/routes/trigger_routes.py`
- **Existing Endpoint**: `POST /api/trigger/crash`
- **Purpose**: Accept custom crash payload data
- **Usage**: For advanced scenarios with custom sensor data

### **4. Updated Startup Messages**
- **File**: `backend/src/app.py`
- **Change**: Shows server is waiting for requests
- **Displays**: Available endpoints

---

## 🚀 How to Use

### **Step 1: Start the Server**
```powershell
python run.py
```

**Output:**
```
Trauma Detection System Started
Server running at: http://0.0.0.0:8000
API Docs at: http://0.0.0.0:8000/docs

Waiting for crash trigger...
  - Frontend button: GET /api/trigger/crash
  - Custom payload: POST /api/trigger/crash
```

### **Step 2: Expose with ngrok**
```powershell
ngrok http 8000
```

**You'll get a URL like:**
```
Forwarding: https://abc123.ngrok.io -> http://localhost:8000
```

### **Step 3: Frontend Button Integration**

Your teammate's frontend should call:
```javascript
// When "Crash Button" is clicked
fetch('https://abc123.ngrok.io/api/trigger/crash', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json'
  }
})
.then(response => response.json())
.then(data => {
  console.log('Crash simulation started:', data);
  // data contains: incident_id, status, gps, etc.
})
.catch(error => {
  console.error('Error:', error);
});
```

---

## 📡 API Endpoints

### **GET /api/trigger/crash** (For Frontend Button)
- **Method**: GET
- **Purpose**: Trigger crash simulation with default test data
- **No Body Required**: Uses default NESCO Centre Goregaon location
- **Response**: `CrashPayloadOutput` with incident details

**Example Response:**
```json
{
  "incident_id": "inc_1234567890_abc123",
  "status": "CRITICAL_EVENT_CONFIRMED",
  "gps": {
    "lat": 19.1680,
    "lon": 72.8500
  },
  "nearest_hospital": "Kokilaben Dhirubhai Ambani Hospital",
  "ambulance_dispatched": true,
  "insurance_preauth_token": "PREAUTH_20251128_ABC123",
  "family_notified": true,
  "timestamp": "2025-11-28T21:40:39.123456"
}
```

### **POST /api/trigger/crash** (For Custom Data)
- **Method**: POST
- **Purpose**: Trigger crash simulation with custom sensor data
- **Body Required**: `CrashPayloadInput` JSON
- **Response**: `CrashPayloadOutput` with incident details

**Example Request:**
```json
{
  "g_force": 5.2,
  "heart_rate": 145.0,
  "heart_rate_after": 45.0,
  "voice_decibels": 0.0,
  "gps": {
    "lat": 19.1680,
    "lon": 72.8500
  },
  "blood_type": "O+",
  "allergies": ["Penicillin"],
  "user_consent": true
}
```

---

## 🔄 Flow

1. **Server Starts**: `python run.py`
2. **Server Waits**: No auto-test, just listening
3. **Frontend Button Clicked**: Frontend sends GET request
4. **Crash Simulation Starts**: Full emergency response protocol
5. **Response Sent**: Frontend receives incident details

---

## ✅ Features Preserved

- ✅ All existing crash detection logic
- ✅ Triangulation (3 confirmations)
- ✅ Multi-agent swarm (Agents A, B, C)
- ✅ Family notifications (email, call, SMS)
- ✅ Hospital finding (Google Maps or mock)
- ✅ Pre-auth token generation
- ✅ Black box recording
- ✅ Phase 3 hospital arrival simulation

---

## 🧪 Testing

### **Test GET Endpoint (Frontend Button)**
```powershell
# Using curl
curl http://localhost:8000/api/trigger/crash

# Or in browser
http://localhost:8000/api/trigger/crash
```

### **Test POST Endpoint (Custom Data)**
```powershell
curl -X POST http://localhost:8000/api/trigger/crash \
  -H "Content-Type: application/json" \
  -d '{
    "g_force": 5.2,
    "heart_rate": 145.0,
    "heart_rate_after": 45.0,
    "voice_decibels": 0.0,
    "gps": {"lat": 19.1680, "lon": 72.8500},
    "blood_type": "O+",
    "allergies": ["Penicillin"],
    "user_consent": true
  }'
```

---

## 📝 Summary

- ✅ **Server waits** for requests (no auto-test)
- ✅ **GET endpoint** for frontend button
- ✅ **POST endpoint** for custom data
- ✅ **All features intact**
- ✅ **Ready for ngrok** integration

Your teammate can now connect the frontend button to trigger the crash simulation!

