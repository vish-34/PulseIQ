# Twilio TTS (Text-to-Speech) - How It Works

## ✅ Good News: No Twilio Console Configuration Needed!

Twilio TTS automatically reads whatever text you send. **The messages are configured in your code**, not in the Twilio console.

---

## 📞 How Twilio TTS Works

When you call `make_call(phone_number, message)`, Twilio:
1. Receives your text message
2. Uses its TTS engine to convert text to speech
3. Calls the phone number
4. Speaks your message using the "alice" voice

**Everything is automatic - no console setup required!**

---

## 📝 Where Messages Are Configured

### **Message 1: Crash Alert Call**
**File:** `backend/src/utils/family_notifications.py` (Lines 47-53)

**Current Message:**
```python
crash_message = (
    f"Emergency Alert. Your family member has undergone a severe accidental crash. "
    f"Emergency services have been alerted and are on the way to the location. "
    f"GPS coordinates: {gps_lat}, {gps_lon}. "
    f"Incident reference number: {incident_id}. "
    f"Patient blood type: {blood_type}. "
    f"Please stay available for further updates. Help is on the way."
)
```

### **Message 2: Hospital Arrival Call**
**File:** `backend/src/utils/family_notifications.py` (Lines 155-160)

**Current Message:**
```python
arrival_message = (
    f"Update: Your family member has arrived at the hospital and is now being admitted. "
    f"Hospital name: {hospital_name}. "
    f"Please check your email for hospital admission fees and detailed information. "
    f"Incident reference number: {incident_id}. "
    f"Medical team is providing care. We will keep you updated."
)
```

---

## 🎯 How to Change What Twilio Says

**Just edit the text in the code!**

1. Open `backend/src/utils/family_notifications.py`
2. Find the message you want to change (line 47 or 155)
3. Edit the text inside the quotes
4. Save the file
5. Restart: `python run.py`

**That's it!** Twilio will automatically speak your new message.

---

## 🔊 Twilio TTS Voice Settings

**Current Voice:** "alice" (default female voice)

**Location:** `backend/src/agents/tools/twilio_service.py` (Line 49)

```python
twiml=f'<Response><Say voice="alice">{escaped_message}</Say></Response>'
```

**Available Voices:**
- `"alice"` - Female, American English (current)
- `"man"` - Male, American English
- `"woman"` - Female, American English
- `"polly.Joanna"` - Female, Neural voice
- `"polly.Matthew"` - Male, Neural voice

**To Change Voice:**
Edit line 49 in `backend/src/agents/tools/twilio_service.py`:
```python
twiml=f'<Response><Say voice="polly.Joanna">{escaped_message}</Say></Response>'
```

---

## 🧪 How to Test/Preview Messages

### Option 1: Check the Logs
When you run `python run.py`, you'll see the exact message in the logs:
```
[TWILIO] Making real Twilio call to +91...
[TWILIO] Call initiated successfully
```

### Option 2: Test with Mock Mode
If Twilio credentials aren't configured, the system shows the message in console:
```
📞 [MOCK CALL] Emergency Call Simulated
Message: Emergency Alert. Your family member has undergone...
```

### Option 3: Use Twilio Console Test
1. Go to https://console.twilio.com
2. Navigate to **Phone Numbers** → **Manage** → **Active Numbers**
3. Click your Twilio number
4. Use the "Test" feature to preview TTS

---

## ✅ Summary

- ✅ **No Twilio console configuration needed**
- ✅ **Messages are in your code** (`family_notifications.py`)
- ✅ **Twilio automatically reads the text** you send
- ✅ **Just edit the code** to change what it says
- ✅ **Voice can be changed** in `twilio_service.py`

**Everything is ready!** The messages are already configured in your code. When you run the system, Twilio will speak exactly what's written in those message variables.

