# Trauma Detection System - Build Prompt for Hackathon

## 🎯 Project Goal
Build a multi-phase emergency response system that detects vehicle crashes, confirms critical events through triangulation, and automatically dispatches emergency services with financial pre-authorization.

## 📋 Demo Configuration (Use These Exact Values)
```
FAMILY_PHONE=+917738187807
FAMILY_EMAIL=rookiedev.mujahid@gmail.com
HOSPITAL_PHONE=+918454030044
HOSPITAL_EMAIL=vishal23borana@gmail.com
GOOGLE_MAPS_API_KEY=[Get from https://console.cloud.google.com/apis/credentials]
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=rookiedev.mujahid@gmail.com
SMTP_PASSWORD=[Gmail App Password - get from https://myaccount.google.com/apppasswords]
```

**Note**: Google Maps finds REAL hospitals. Hospital phone/email from Google Maps takes priority, but use HOSPITAL_PHONE/HOSPITAL_EMAIL as fallback for demo.

## 🏗️ Build Instructions (Divide into Parts)

### **PART 1: Core Detection Layer**
Build these files in order:
1. `backend/src/schemas/crash_payload.py` - Pydantic models:
   - `GPSLocation` (lat, lon)
   - `CrashPayloadInput` (g_force, heart_rate, heart_rate_after, voice_decibels, gps, blood_type, allergies, user_consent)
   - `CrashPayloadOutput` (incident_id, status, gps, nearest_hospital, ambulance_dispatched, insurance_preauth_token, family_notified, timestamp)
   - Use `pattern=` not `regex=` for Pydantic v2

2. `backend/src/agents/core/crash_detector.py` - Triangulation logic:
   - `check_impact(gforce)` - returns True if > 4.0G
   - `check_heart_change(hr, hr_after)` - returns True if spike >140 then drop <50 or None
   - `check_silence(decibels)` - returns True if == 0
   - `triangulate(payload)` - requires ALL 3 confirmations

3. `backend/src/agents/core/state_machine.py` - State management:
   - States: idle → triage → cancel_window → confirmed → dispatching → hospital_mode → closed
   - Methods: start_triage(), start_cancel_window(), confirm_critical_event(), activate_protocol(), enter_hospital_mode()

### **PART 2: Tools & Services**
4. `backend/src/config/settings.py` - Configuration with Pydantic Settings:
   - Include FAMILY_PHONE, FAMILY_EMAIL, HOSPITAL_PHONE, HOSPITAL_EMAIL
   - SMTP settings, thresholds, timeouts

5. `backend/src/agents/tools/maps_service.py` - Hospital lookup:
   - `find_nearest_trauma_center(gps)` - Uses Google Maps Places API to find REAL nearest trauma center
   - Calls: `https://maps.googleapis.com/maps/api/place/nearbysearch/json` with type=hospital, keyword=trauma center
   - Gets place details via `https://maps.googleapis.com/maps/api/place/details/json` for phone/address
   - Returns real hospital data: name, address, phone (from Google), email (from Google or fallback to settings.HOSPITAL_EMAIL)
   - **IMPORTANT**: If Google Maps returns hospital phone/email, use those. Otherwise use settings.HOSPITAL_PHONE and settings.HOSPITAL_EMAIL as fallback
   - Mock fallback only if no API key AND no settings configured

6. `backend/src/agents/tools/twilio_service.py` - Calls/SMS:
   - `make_call()`, `send_sms()`, `make_emergency_call()` - use settings.HOSPITAL_PHONE
   - Mock mode if no Twilio credentials (print to console)

7. `backend/src/agents/tools/email_service.py` - Email sending:
   - `send_preauth_email()` - sends to hospital_email from settings
   - `send_family_notification()` - sends to family_email from settings
   - **CRITICAL**: Check `if settings.SMTP_HOST and settings.SMTP_USER and settings.SMTP_PASSWORD:` FIRST, then send real email via `_send_via_smtp()`, else mock

8. `backend/src/utils/qr_generator.py` - QR code generation:
   - `generate_medical_qr(medical_data)` - returns PNG bytes
   - `generate_first_responder_dashboard_data()` - returns HTML

### **PART 3: Insurance Layer**
9. `backend/src/agents/insurance/policy_lookup.py` - Mock policy database
10. `backend/src/agents/insurance/preauth_generator.py` - Token generation (PREAUTH_YYYYMMDD_RANDOM6)

### **PART 4: Multi-Agent Swarm**
11. `backend/src/agents/dispatcher/dispatcher_agent.py` - Agent A:
    - Finds REAL hospital via Google Maps API (gets actual hospital name, address, phone from Google)
    - Calls emergency dispatcher: Use hospital phone from Google Maps if available, else use `settings.HOSPITAL_PHONE` (+918454030044)
    - Sends "Ghost Voice" alert with real hospital details

12. `backend/src/agents/guardian/guardian_agent.py` - Agent B:
    - Generates QR code, dashboard, black box recording

13. `backend/src/agents/treasurer/treasurer_agent.py` - Agent C:
    - Looks up policy, generates pre-auth token
    - Emails to: Use hospital email from Google Maps if available, else use `settings.HOSPITAL_EMAIL` (vishal23borana@gmail.com)

14. `backend/src/agents/core/master_agent.py` - Orchestrator:
    - Runs all 3 agents in parallel using `asyncio.gather()`

### **PART 5: API Layer**
15. `backend/src/utils/id_generator.py` - Generate incident IDs
16. `backend/src/models/incident_model.py` - In-memory storage
17. `backend/src/controllers/trigger_controller.py` - Main flow:
    - Creates incident, runs triangulation, activates Phase 2 if confirmed
18. `backend/src/controllers/status_controller.py` - Status endpoints
19. `backend/src/routes/trigger_routes.py` - POST /api/trigger/crash
20. `backend/src/routes/agent_routes.py` - Status/logs endpoints
21. `backend/src/app.py` - FastAPI app with auto-test mode:
    - Add `--auto-test` flag support
    - Auto-trigger test on startup if flag present

### **PART 6: Testing**
22. `backend/src/test_email_direct.py` - Direct email test
23. `backend/src/run.py` - Simple runner with auto-test

## ⚠️ Critical Requirements
- **Google Maps Integration**: Use REAL Google Maps Places API to find nearest trauma center. Get actual hospital name, address, phone from Google. Only use settings.HOSPITAL_PHONE/EMAIL as fallback if Google doesn't provide them.

- **Email Logic**: Must check if SMTP is configured FIRST, then send real emails. Don't go to mock if credentials exist.

- **Phone Numbers**: 
  - Hospital: Use Google Maps hospital phone if available, else `settings.HOSPITAL_PHONE` (+918454030044)
  - Family: Always use `settings.FAMILY_PHONE` (+917738187807)

- **Email Addresses**: 
  - Hospital: Use Google Maps hospital email if available, else `settings.HOSPITAL_EMAIL` (vishal23borana@gmail.com)
  - Family: Always use `settings.FAMILY_EMAIL` (rookiedev.mujahid@gmail.com)

- **Pydantic v2**: Use `pattern=` not `regex=`, use `@field_validator` not `@validator`

- **Async/Await**: All I/O operations must be async

- **Error Handling**: Graceful fallbacks, don't crash on errors

## 🚀 Final Steps
1. Create `.env` file with demo configuration above
2. Install dependencies: `pip install -r requirements.txt`
3. Run: `python backend/src/run.py`
4. System auto-triggers test, sends emails to configured addresses

## 📦 Required Dependencies
```
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
pydantic>=2.10.0
pydantic-settings>=2.6.0
httpx>=0.25.1
qrcode[pil]>=7.4.2
Pillow>=12.0.0
python-dotenv>=1.0.0
```

## 🗺️ Google Maps API Setup
1. Go to: https://console.cloud.google.com/apis/credentials
2. Create new project or select existing
3. Enable "Places API" and "Maps JavaScript API"
4. Create API Key (restrict to Places API for security)
5. Add to `.env`: `GOOGLE_MAPS_API_KEY=your_api_key_here`
6. **For demo**: If no API key, system falls back to mock hospital but still uses configured phone/email

## ✅ Success Criteria
- Server starts without errors
- Auto-test triggers on `python run.py`
- Emails sent to vishal23borana@gmail.com and rookiedev.mujahid@gmail.com
- All 3 agents execute in parallel
- Pre-auth token generated and emailed
- Console shows all agent activities

**Build one part at a time, test after each part, then move to next.**

