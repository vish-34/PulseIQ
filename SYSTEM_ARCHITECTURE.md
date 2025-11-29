# Trauma Detection System - Complete Architecture Breakdown

## 📋 System Overview

A multi-phase emergency response system that detects vehicle crashes, confirms critical events through triangulation, and automatically dispatches emergency services with financial pre-authorization.

---

## 🏗️ SYSTEM ARCHITECTURE - DIVIDED INTO PARTS

### **PART 1: CORE DETECTION LAYER** ✅ (COMPLETED)

**Location:** `backend/src/agents/core/`

#### 1.1 Crash Detector (`crash_detector.py`)
**Purpose:** Phase 1 - Triangulation Trigger (0-10 seconds)

**Components:**
- `check_impact(gforce: float) -> bool`
  - Threshold: G-Force > 4.0
  - Detects accelerometer impact
  
- `check_heart_change(hr: float, hr_after: Optional[float]) -> bool`
  - Detects: HR spike (>140 BPM) → drop (<50 BPM) or silence
  - Pattern: Shock → Unconsciousness
  
- `check_silence(decibels: float) -> bool`
  - Threshold: voice_decibels == 0
  - Consciousness test result
  
- `triangulate(payload: CrashPayloadInput) -> tuple[bool, str]`
  - **Main Logic Gate**
  - Requires ALL 3 confirmations
  - Returns: `(True, "CRITICAL_EVENT_CONFIRMED")` or `(False, "MONITOR_MODE - ...")`

**Input:** `CrashPayloadInput` (from schemas)
**Output:** Boolean confirmation + status message

---

#### 1.2 State Machine (`state_machine.py`)
**Purpose:** Manages incident lifecycle and state transitions

**Components:**
- `IncidentState` class
- States: `idle` → `triage` → `cancel_window` → `confirmed` → `dispatching` → `hospital_mode` → `closed`
- Methods:
  - `start_triage(payload)` - Impact detected
  - `start_cancel_window()` - Consciousness test (5 sec)
  - `confirm_critical_event()` - All 3 confirmations met
  - `cancel_incident(reason)` - User responded / false alarm
  - `activate_protocol()` - Phase 2 trigger
  - `enter_hospital_mode(hospital_gps)` - Phase 3 trigger
  - `close_incident(reason)` - Resolution

**Features:**
- State transition validation
- Comprehensive logging
- Payload storage
- Metadata tracking

---

### **PART 2: DATA SCHEMAS LAYER** ✅ (COMPLETED)

**Location:** `backend/src/schemas/`

#### 2.1 Crash Payload Schema (`crash_payload.py`)
**Purpose:** Input/Output validation and type safety

**Components:**
- `GPSLocation` - Lat/Lon coordinates
- `CrashPayloadInput` - Input schema:
  - `g_force`, `heart_rate`, `heart_rate_after`
  - `voice_decibels`, `gps`, `blood_type`
  - `allergies`, `user_consent`
  
- `CrashPayloadOutput` - Response schema:
  - `incident_id`, `status`, `gps`
  - `nearest_hospital`, `ambulance_dispatched`
  - `insurance_preauth_token`, `family_notified`
  - `timestamp`

- `SensorData` - Real-time monitoring
- `UserMedicalProfile` - Extended medical info

---

### **PART 3: MULTI-AGENT SWARM LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/agents/`

#### 3.1 Agent A: The Dispatcher (Logistics)
**File:** `backend/src/agents/dispatcher/dispatcher_agent.py` (NEW)

**Responsibilities:**
- Find nearest trauma center (Google Maps API)
- Call Ambulance API (108 / Emergency Services)
- Send "Ghost Voice" message to dispatcher
- Format: `"Automated Alert. Severe Crash at [Lat/Long]. User Unresponsive. Blood Type O+. Dispatch ACLS unit."`

**Dependencies:**
- `tools/maps_service.py` - Hospital lookup
- `tools/twilio_service.py` - Emergency call
- `schemas/crash_payload.py` - GPS, blood type

**Methods:**
```python
async def find_nearest_trauma_center(gps: GPSLocation) -> dict
async def dispatch_ambulance(location: GPSLocation, medical_info: dict) -> bool
async def send_ghost_voice_alert(dispatcher_number: str, message: str) -> bool
```

---

#### 3.2 Agent B: The Guardian (Medical Data)
**File:** `backend/src/agents/guardian/guardian_agent.py` (NEW)

**Responsibilities:**
- Override lock screen (force screen ON)
- Display "First Responder Dashboard"
- Generate QR Code with:
  - Allergies
  - Blood Type
  - Current Vitals
  - Emergency Contact
- Start audio recording (Black Box mode)
- Store evidence for legal purposes

**Dependencies:**
- `models/user_model.py` - User medical profile
- `schemas/crash_payload.py` - Medical data
- `utils/qr_generator.py` - QR code generation (NEW)

**Methods:**
```python
def override_lock_screen() -> bool
def generate_first_responder_dashboard(payload: CrashPayloadInput) -> str
def generate_medical_qr_code(medical_data: dict) -> bytes
def start_black_box_recording(incident_id: str) -> str
```

---

#### 3.3 Agent C: The Treasurer (Financial)
**File:** `backend/src/agents/treasurer/treasurer_agent.py` (NEW)

**Responsibilities:**
- Connect to Insurance API (mock)
- Generate Pre-Auth Token (₹50,000)
- Email token to Hospital Reception
- Solve: "Hospitals refusing entry without deposit"

**Dependencies:**
- `agents/insurance/policy_lookup.py` - Policy verification
- `agents/insurance/preauth_generator.py` - Token generation
- `tools/email_service.py` - Email delivery

**Methods:**
```python
async def lookup_insurance_policy(user_id: str) -> dict
async def generate_preauth_token(amount: float, hospital_id: str) -> str
async def email_preauth_to_hospital(hospital_email: str, token: str, user_info: dict) -> bool
```

---

### **PART 4: TOOLS & SERVICES LAYER** ⚠️ (PARTIALLY BUILT)

**Location:** `backend/src/agents/tools/`

#### 4.1 Maps Service (`maps_service.py`) - EMPTY
**Purpose:** Google Maps API integration

**Required Methods:**
```python
async def find_nearest_trauma_center(lat: float, lon: float) -> dict:
    # Returns: {name, address, phone, email, gps: {lat, lon}, distance_km}
    
async def get_directions(origin: GPSLocation, destination: GPSLocation) -> dict:
    # Returns: {distance_km, duration_minutes, route}
```

**API Integration:**
- Google Maps Places API (Nearby Search)
- Filter: `type=hospital` + `keyword=trauma center`

---

#### 4.2 Twilio Service (`twilio_service.py`) - PARTIAL
**Purpose:** Emergency calls and SMS

**Current:** Only has `make_call()` stub

**Required Methods:**
```python
async def make_call(phone_number: str, message: str) -> bool:
    # TTS (Text-to-Speech) call to dispatcher
    # "Automated Alert. Severe Crash at [location]..."
    
async def send_sms(phone_number: str, message: str) -> bool:
    # SMS to family/emergency contact
    
async def make_emergency_call(dispatcher_number: str, alert_data: dict) -> bool:
    # Structured emergency call with TTS
```

**Integration:**
- Twilio Voice API (TTS)
- Twilio SMS API

---

#### 4.3 Email Service (`email_service.py`) - EMPTY
**Purpose:** Send pre-auth tokens to hospitals

**Required Methods:**
```python
async def send_preauth_email(
    hospital_email: str,
    token: str,
    user_info: dict,
    amount: float
) -> bool:
    # Email template with:
    # - Pre-auth token
    # - User details
    # - Amount authorized
    # - Incident ID
    
async def send_family_notification(
    family_email: str,
    incident_info: dict
) -> bool:
    # "User has arrived at City Hospital. Vitals are stable."
```

**Integration:**
- SMTP (Gmail/SendGrid) or
- SendGrid API

---

### **PART 5: INSURANCE LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/agents/insurance/`

#### 5.1 Policy Lookup (`policy_lookup.py`) - EMPTY
**Purpose:** Verify user insurance policy

**Required Methods:**
```python
async def lookup_policy(user_id: str) -> dict:
    # Returns: {policy_number, provider, coverage_amount, active}
    
async def verify_coverage(amount: float, policy_number: str) -> bool:
    # Check if amount is within coverage
```

**Mock Implementation:**
- In-memory policy database
- Or external API integration

---

#### 5.2 Pre-Auth Generator (`preauth_generator.py`) - EMPTY
**Purpose:** Generate pre-authorization tokens

**Required Methods:**
```python
async def generate_preauth_token(
    policy_number: str,
    amount: float,
    hospital_id: str,
    incident_id: str
) -> str:
    # Returns: Unique token (e.g., "PREAUTH_20241201_ABC123")
    # Format: PREAUTH_{timestamp}_{random}
    
async def validate_token(token: str) -> dict:
    # Returns: {valid, amount, hospital_id, expires_at}
```

**Token Format:**
- `PREAUTH_{YYYYMMDD}_{RANDOM6}`
- Expires: 24 hours
- Amount: ₹50,000 (configurable)

---

### **PART 6: MASTER AGENT ORCHESTRATOR** ⚠️ (TO BE BUILT)

**Location:** `backend/src/agents/core/`

#### 6.1 Master Agent (`master_agent.py`) - NEW
**Purpose:** Orchestrate all 3 sub-agents in parallel

**Responsibilities:**
- Wake up Agent A, B, C simultaneously
- Coordinate parallel execution
- Aggregate results
- Handle failures gracefully

**Methods:**
```python
async def activate_swarm(payload: CrashPayloadInput, incident_id: str) -> dict:
    # Parallel execution:
    # - task_a = dispatcher_agent.run(...)
    # - task_b = guardian_agent.run(...)
    # - task_c = treasurer_agent.run(...)
    # Returns: {dispatcher_result, guardian_result, treasurer_result}
    
async def handle_phase_2(incident_state: IncidentState) -> dict:
    # Main entry point for Phase 2
    # Calls activate_swarm()
    # Updates state machine
```

**Integration:**
- `asyncio.gather()` for parallel execution
- Error handling per agent
- Timeout management (30 seconds max)

---

### **PART 7: PHASE 3 HANDOFF LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/agents/handoff/`

#### 7.1 Hospital Arrival Handler (`hospital_handler.py`) - NEW
**Purpose:** Detect arrival and switch to Hospital Mode

**Responsibilities:**
- Monitor GPS location
- Match phone GPS with Hospital GPS
- Switch state machine to `hospital_mode`
- Send family notification

**Methods:**
```python
async def monitor_arrival(
    current_gps: GPSLocation,
    hospital_gps: GPSLocation,
    incident_id: str
) -> bool:
    # Check if distance < 100 meters
    # If match: trigger hospital_mode
    
async def send_arrival_notification(
    family_contact: str,
    hospital_info: dict,
    incident_id: str
) -> bool:
    # "User has arrived at City Hospital. Vitals are stable. Ward number pending."
```

**GPS Matching:**
- Distance threshold: 100 meters
- Continuous monitoring (every 5 seconds)

---

### **PART 8: API & CONTROLLER LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/controllers/` & `backend/src/routes/`

#### 8.1 Trigger Controller (`trigger_controller.py`) - EMPTY
**Purpose:** Handle crash detection trigger endpoint

**Endpoints:**
```python
POST /api/trigger/crash
Body: CrashPayloadInput
Response: CrashPayloadOutput

Flow:
1. Validate payload
2. Create incident (incident_model.py)
3. Initialize state machine
4. Run triangulation (crash_detector.py)
5. If confirmed: activate Phase 2 (master_agent.py)
6. Return response
```

---

#### 8.2 Status Controller (`status_controller.py`) - EMPTY
**Purpose:** Get incident status

**Endpoints:**
```python
GET /api/incident/{incident_id}/status
Response: {state, logs, metadata, timestamp}

GET /api/incident/{incident_id}/logs
Response: List of log entries
```

---

#### 8.3 Routes (`trigger_routes.py`, `agent_routes.py`) - EMPTY
**Purpose:** FastAPI route definitions

**Required Routes:**
- `POST /api/trigger/crash` - Crash detection
- `GET /api/incident/{id}/status` - Status check
- `GET /api/incident/{id}/logs` - Log retrieval
- `POST /api/incident/{id}/cancel` - Cancel incident

---

### **PART 9: DATA MODELS LAYER** ⚠️ (PARTIALLY BUILT)

**Location:** `backend/src/models/`

#### 9.1 Incident Model (`incident_model.py`) - PARTIAL
**Current:** Basic in-memory storage

**Needed:**
- Integration with state machine
- Database persistence (optional)
- Better structure

#### 9.2 User Model (`user_model.py`) - COMPLETE
**Status:** ✅ Has basic structure

**May Need:**
- Database integration
- Medical profile extension

---

### **PART 10: UTILITIES LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/utils/`

#### 10.1 QR Code Generator (`qr_generator.py`) - NEW
**Purpose:** Generate medical QR codes for first responders

**Methods:**
```python
def generate_medical_qr(medical_data: dict) -> bytes:
    # JSON payload: {blood_type, allergies, emergency_contact, vitals}
    # Returns: PNG image bytes
```

**Library:** `qrcode` (Python)

---

#### 10.2 ID Generator (`id_generator.py`) - EXISTS
**Purpose:** Generate unique incident IDs

**Check:** Verify implementation

---

#### 10.3 Logger (`logger.py`) - EXISTS
**Purpose:** Structured logging

**Check:** Verify implementation

---

### **PART 11: CONFIGURATION LAYER** ⚠️ (TO BE BUILT)

**Location:** `backend/src/config/`

#### 11.1 Settings (`settings.py`) - EMPTY
**Purpose:** Environment variables and configuration

**Required:**
```python
# API Keys
GOOGLE_MAPS_API_KEY: str
TWILIO_ACCOUNT_SID: str
TWILIO_AUTH_TOKEN: str
SENDGRID_API_KEY: str (optional)

# Thresholds
G_FORCE_THRESHOLD: float = 4.0
HEART_RATE_SPIKE: float = 140.0
HEART_RATE_DROP: float = 50.0

# Financial
DEFAULT_PREAUTH_AMOUNT: float = 50000.0  # ₹50,000

# GPS
HOSPITAL_ARRIVAL_THRESHOLD_METERS: float = 100.0
```

---

#### 11.2 Database (`db.py`) - EMPTY
**Purpose:** Database connection (if using DB)

**Optional:** SQLite/PostgreSQL for persistence

---

### **PART 12: MAIN APPLICATION** ⚠️ (TO BE BUILT)

**Location:** `backend/src/app.py` - EMPTY

**Purpose:** FastAPI application entry point

**Required:**
```python
from fastapi import FastAPI
from routes.trigger_routes import router as trigger_router
from routes.agent_routes import router as agent_router

app = FastAPI(title="Trauma Detection System")

app.include_router(trigger_router, prefix="/api/trigger")
app.include_router(agent_router, prefix="/api")

@app.get("/")
def health_check():
    return {"status": "operational"}
```

---

## 🔄 COMPLETE FLOW DIAGRAM

```
[PHONE/SMARTWATCH SENSORS]
         ↓
[CrashPayloadInput] → POST /api/trigger/crash
         ↓
[Trigger Controller] → Validate & Create Incident
         ↓
[State Machine] → idle → triage
         ↓
[Crash Detector] → triangulate()
    ├─ check_impact() → G-Force > 4G?
    ├─ check_heart_change() → HR spike → drop?
    └─ check_silence() → voice_decibels == 0?
         ↓
[If ALL 3 confirmed]
         ↓
[State Machine] → cancel_window (5 sec wait)
         ↓
[If no voice response]
         ↓
[State Machine] → confirmed
         ↓
[Master Agent] → activate_swarm() [PARALLEL]
    ├─ Agent A (Dispatcher)
    │   ├─ Maps Service → Find Hospital
    │   └─ Twilio Service → Call 108
    │
    ├─ Agent B (Guardian)
    │   ├─ Generate QR Code
    │   ├─ Override Lock Screen
    │   └─ Start Black Box Recording
    │
    └─ Agent C (Treasurer)
        ├─ Policy Lookup
        ├─ Generate Pre-Auth Token
        └─ Email Service → Send to Hospital
         ↓
[State Machine] → dispatching
         ↓
[GPS Monitoring] → Check if arrived at hospital
         ↓
[If GPS match (< 100m)]
         ↓
[State Machine] → hospital_mode
         ↓
[Family Notification] → SMS/Email
         ↓
[State Machine] → closed (when resolved)
```

---

## 📊 BUILD PRIORITY ORDER

### **Phase 1: Foundation** ✅ (DONE)
1. ✅ Crash Detector
2. ✅ State Machine
3. ✅ Schemas

### **Phase 2: Core Services** (HIGH PRIORITY)
1. Maps Service (Google Maps API)
2. Twilio Service (Complete implementation)
3. Email Service
4. Master Agent Orchestrator

### **Phase 3: Sub-Agents** (HIGH PRIORITY)
1. Agent A: Dispatcher
2. Agent B: Guardian (QR Code + Lock Screen)
3. Agent C: Treasurer (Insurance + Pre-Auth)

### **Phase 4: Handoff** (MEDIUM PRIORITY)
1. Hospital Arrival Handler
2. GPS Monitoring Service

### **Phase 5: API Layer** (MEDIUM PRIORITY)
1. Trigger Controller
2. Status Controller
3. Routes

### **Phase 6: Utilities** (LOW PRIORITY)
1. QR Code Generator
2. Configuration
3. Main App Setup

---

## 🎯 KEY INTEGRATION POINTS

1. **State Machine ↔ Crash Detector**: State transitions based on triangulation results
2. **Master Agent ↔ Sub-Agents**: Parallel execution coordination
3. **Sub-Agents ↔ Tools**: Service layer integration
4. **Controller ↔ State Machine**: API endpoint to state management
5. **GPS Monitoring ↔ State Machine**: Hospital arrival detection

---

## 📝 NOTES FOR IMPLEMENTATION

- **Async/Await**: All I/O operations should be async
- **Error Handling**: Each agent should handle failures gracefully
- **Logging**: Comprehensive logging at every step
- **Mocking**: Insurance API can be mocked for demo
- **Visual Demo**: Terminal logs scrolling in real-time
- **Audio Demo**: Synthetic voice call to dispatcher

---

**Total Components:** ~25 files
**Completed:** 3 files (12%)
**Remaining:** 22 files (88%)

