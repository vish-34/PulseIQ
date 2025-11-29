# How to Customize Phone Call Messages

## 📞 Where Call Messages Are Defined

All phone call messages are in: **`backend/src/utils/family_notifications.py`**

---

## 🚨 Message 1: Crash Alert Call (When Crash is Confirmed)

**Location:** Lines 47-53 in `family_notifications.py`

**Current Message:**
```python
crash_message = (
    f"Emergency Alert. A crash has been detected. "
    f"Emergency services are being dispatched. "
    f"Location: {gps_lat}, {gps_lon}. "
    f"Incident ID: {incident_id}. "
    f"Blood type: {blood_type}."
)
```

**To Customize:**
Edit `backend/src/utils/family_notifications.py` around line 47:

```python
# Prepare crash alert message
crash_message = (
    f"Your custom message here. "
    f"Location: {gps_lat}, {gps_lon}. "
    f"Incident ID: {incident_id}."
)
```

**Available Variables:**
- `incident_id` - The incident ID
- `gps_lat` - GPS latitude
- `gps_lon` - GPS longitude  
- `blood_type` - Patient blood type

---

## 🏥 Message 2: Hospital Arrival Call (When User Reaches Hospital)

**Location:** Line 155 in `family_notifications.py`

**Current Message:**
```python
arrival_message = "User has reached the trauma center. Stabilization in progress."
```

**To Customize:**
Edit `backend/src/utils/family_notifications.py` around line 155:

```python
# Prepare hospital arrival message
arrival_message = (
    f"Your custom message here. "
    f"Patient has arrived at {hospital_name}. "
    f"Incident ID: {incident_id}."
)
```

**Available Variables:**
- `incident_id` - The incident ID
- `hospital_name` - Hospital name
- `hospital_gps_lat` - Hospital GPS latitude
- `hospital_gps_lon` - Hospital GPS longitude

---

## 📝 Example Custom Messages

### Example 1: More Personal Crash Alert
```python
crash_message = (
    f"URGENT: A vehicle crash has been detected involving your family member. "
    f"Emergency services are on the way. "
    f"Location coordinates: {gps_lat}, {gps_lon}. "
    f"Reference number: {incident_id}. "
    f"Please stay available for updates."
)
```

### Example 2: Detailed Hospital Arrival
```python
arrival_message = (
    f"Update: Your family member has safely arrived at {hospital_name}. "
    f"Medical team is providing care. "
    f"Incident reference: {incident_id}. "
    f"Further updates will be provided as available."
)
```

### Example 3: Simple & Clear
```python
crash_message = (
    f"EMERGENCY: Crash detected at {gps_lat}, {gps_lon}. "
    f"Help is on the way. ID: {incident_id}."
)

arrival_message = (
    f"Patient arrived at hospital. Medical care in progress. ID: {incident_id}."
)
```

---

## ⚠️ Important Notes

1. **Keep it concise**: Phone calls have time limits. Keep messages under 30-40 seconds when spoken.

2. **Test pronunciation**: Twilio TTS will read your message. Avoid:
   - Special characters that don't read well
   - Very long numbers without breaks
   - Complex abbreviations

3. **Use f-strings**: To include variables, use `f"text {variable}"` format.

4. **After editing**: Save the file and restart the server:
   ```powershell
   python run.py
   ```

---

## 🎯 Quick Edit Guide

1. Open: `backend/src/utils/family_notifications.py`
2. Find line 47 for crash message
3. Find line 155 for arrival message
4. Edit the text between quotes
5. Save the file
6. Restart: `python run.py`

That's it! Your custom messages will be used in the next call.

