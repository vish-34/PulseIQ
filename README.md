# Trauma Detection System

A multi-phase emergency response system that detects vehicle crashes, confirms critical events through triangulation, and automatically dispatches emergency services with financial pre-authorization.

## 🚀 Features

### Phase 1: Triangulation Trigger (0-10 seconds)
- **3-Confirmation System** to prevent false alarms:
  1. Sensor Input: G-Force > 4G (Impact detection)
  2. Biometric Check: Heart Rate spike (>140 BPM) → drop (<50 BPM) or silence
  3. Consciousness Test: No voice detected (5-second listening window)

### Phase 2: Multi-Agent Swarm (10-30 seconds)
Three agents work in parallel:
- **Agent A (Dispatcher)**: Finds nearest trauma center, calls emergency services
- **Agent B (Guardian)**: Generates medical QR code, overrides lock screen, starts black box recording
- **Agent C (Treasurer)**: Looks up insurance, generates pre-auth token (₹50,000), emails hospital

### Phase 3: Hospital Arrival Handoff
- GPS monitoring for hospital arrival
- Automatic family notification
- State machine transitions

## 📦 Installation

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables (create .env file)
cp .env.example .env
# Edit .env with your API keys
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
# API Keys (Optional - system works in mock mode without them)
GOOGLE_MAPS_API_KEY=your_google_maps_key
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+1234567890

# Email (Optional)
SENDGRID_API_KEY=your_sendgrid_key
# OR
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password

# Emergency Services
EMERGENCY_DISPATCHER_NUMBER=108
```

## 🏃 Running the System

```bash
# From backend/src directory
cd backend/src
python app.py

# Or using uvicorn directly
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

## 📡 API Endpoints

### Trigger Crash Detection
```bash
POST /api/trigger/crash
Content-Type: application/json

{
  "g_force": 5.2,
  "heart_rate": 145.0,
  "heart_rate_after": 45.0,
  "voice_decibels": 0.0,
  "gps": {
    "lat": 19.0760,
    "lon": 72.8777
  },
  "blood_type": "O+",
  "allergies": ["Penicillin"],
  "user_consent": true
}
```

### Get Incident Status
```bash
GET /api/incident/{incident_id}/status
```

### Get Incident Logs
```bash
GET /api/incident/{incident_id}/logs?limit=10
```

### Cancel Incident
```bash
POST /api/incident/{incident_id}/cancel
{
  "reason": "User responded"
}
```

## 🏗️ Architecture

See `SYSTEM_ARCHITECTURE.md` for complete system breakdown.

## 📝 Notes

- **Mock Mode**: System works without API keys (uses mock data)
- **Async Operations**: All I/O operations are async for maximum performance
- **State Machine**: Comprehensive state management with logging
- **Error Handling**: Graceful degradation if services are unavailable

## 🎯 Demo Scenario

1. User crashes → Sensors detect impact
2. System confirms critical event (3 confirmations)
3. Multi-agent swarm activates (parallel execution)
4. Ambulance dispatched, hospital notified, pre-auth sent
5. User arrives at hospital → Family notified

## 📄 License

MIT

