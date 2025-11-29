from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, datetime
from google import genai
from google.genai import types

app = Flask(__name__)
CORS(app)

API_KEY = os.environ.get("GOOGLE_API_KEY", "AIzaSyBFd_Qfrtp_0VPBxWQe6hkX-Bu44W5tolM")
MODEL_ID = "gemini-2.5-flash"
VITALS_FILE = "wearable_data.json"
ACTIVITY_FILE = "activity.json"

client = genai.Client(api_key=API_KEY)

uploaded_pdf = None
pending_appointment = {}
latest_alert = None 

# ⭐ NEW: Stores the last alert question sent to the user so we don't lose context
active_alert_context = None 

# ------------------------------------------------------
# 🏥 DOCTOR DATABASE
# ------------------------------------------------------
doctors = [
    {"name": "Dr. Arvind Sharma", "specialty": "Endocrinologist", "keyword": ["glucose", "sugar", "diabetes"]},
    {"name": "Dr. Rhea Kapur", "specialty": "Cardiologist", "keyword": ["heart", "bp", "blood pressure", "palpitations"]},
    {"name": "Dr. Sameer Iqbal", "specialty": "Pulmonologist", "keyword": ["breath", "lungs", "oxygen", "spo2"]},
    {"name": "Dr. Aditi Verma", "specialty": "Dietician", "keyword": ["cholesterol", "diet", "weight", "bmi"]},
    {"name": "Dr. Karan Patel", "specialty": "Neurologist", "keyword": ["headache", "dizzy", "nerves"]},
    {"name": "Dr. Meera Desai", "specialty": "General Physician", "keyword": []}
]

def pick_doctor(message):
    msg = message.lower()
    for doc in doctors:
        if any(kw in msg for kw in doc["keyword"]):
            return doc
    return doctors[-1]

# ------------------------------------------------------
# SYSTEM INSTRUCTION
# ------------------------------------------------------
system_instruction = (
    "You are Dr. AI, an experienced, empathetic, and warm General Physician.\n"
    "Your goal is to care for the patient, not just answer questions.\n"
    "1. **Persona:** Speak naturally, like a caring family doctor. Never say 'As an AI'.\n"
    "2. **Context:** You have access to the patient's vitals. ALWAYS look at them.\n"
    "3. **Tone:** Be professional but conversational.\n"
    "4. **Brevity:** Keep answers concise (2-3 sentences) but meaningful.\n"
)

# ------------------------------------------------------
# ACTIVITY LOGGING
# ------------------------------------------------------
def log_activity(label):
    entry = {
        "label": label,
        "time": datetime.datetime.now().strftime("%I:%M %p • %d %b %Y")
    }
    if os.path.exists(ACTIVITY_FILE):
        with open(ACTIVITY_FILE, "r") as f:
            data = json.load(f)
    else:
        data = []
    data.insert(0, entry)
    with open(ACTIVITY_FILE, "w") as f:
        json.dump(data, f, indent=2)

@app.route("/get_activity", methods=["GET"])
def get_activity():
    if not os.path.exists(ACTIVITY_FILE):
        return jsonify([])
    with open(ACTIVITY_FILE, "r") as f:
        return jsonify(json.load(f))

# ------------------------------------------------------
# ⭐ TRIAGE LOGIC
# ------------------------------------------------------
def check_vital_alert(vitals):
    global latest_alert

    glucose = vitals.get("glucose")
    spo2 = vitals.get("spo2")
    hr = vitals.get("heart_rate")
    sys = vitals.get("systolic")
    dia = vitals.get("diastolic")
    temp = vitals.get("temperature")

    # PRIORITY 1: Oxygen
    if spo2 and spo2 < 92:
        latest_alert = f"I noticed your oxygen is quite low ({spo2}%). Are you finding it hard to breathe right now?"
        return

    # PRIORITY 2: Glucose
    if glucose:
        if glucose > 200:
            latest_alert = f"Hey, I see your glucose spiked to {glucose}. Did you miss a dose or eat something sweet recently?"
            return
        if glucose < 70:
            latest_alert = f"Your sugar levels are dropping ({glucose}). Please grab some juice or candy. Are you feeling shaky?"
            return

    # PRIORITY 3: BP
    if sys and dia:
        if sys > 160 or dia > 100:
            latest_alert = f"Your blood pressure is reading {sys}/{dia}, which is high. Are you feeling a headache or dizziness?"
            return
        if sys < 90:
            latest_alert = f"Your BP is a bit low ({sys}/{dia}). You might feel lightheaded—have you had enough water today?"
            return
    
    # PRIORITY 4: Heart Rate
    if hr and hr > 120:
        latest_alert = f"Your heart rate is racing at {hr} BPM. Are you exercising, or do you feel palpitations?"
        return

    latest_alert = None

@app.route('/check_alert', methods=['GET'])
def check_alert():
    global latest_alert, active_alert_context
    if latest_alert:
        msg = latest_alert
        latest_alert = None
        # ⭐ SAVE CONTEXT: Remember what we just asked the user
        active_alert_context = msg 
        return jsonify({"alert": msg})
    return jsonify({"alert": None})

# ------------------------------------------------------
# UPDATE VITALS
# ------------------------------------------------------
@app.route('/update_vitals', methods=['POST'])
def update_vitals():
    global latest_alert
    vitals = request.json
    if not vitals:
        return jsonify({"response": "No vitals received."}), 400

    with open(VITALS_FILE, "w") as f:
        json.dump(vitals, f, indent=2)

    check_vital_alert(vitals)

    return jsonify({"response": "Vitals updated."})

# ------------------------------------------------------
# UPLOAD PDF
# ------------------------------------------------------
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    global uploaded_pdf
    file = request.files.get("file")
    if not file:
        return jsonify({"response": "No PDF uploaded."}), 400
    temp_path = "uploaded_report.pdf"
    file.save(temp_path)
    try:
        uploaded_pdf = client.files.upload(file=temp_path)
    except Exception as e:
        return jsonify({"response": f"PDF upload failed: {str(e)}"}), 500
    log_activity("📄 Uploaded a medical report")
    return jsonify({"response": "I've received your report. I'm reading through it now—what would you like to know?"})

# ------------------------------------------------------
# ⭐ CHAT LOGIC (WITH CONTEXT REPAIR)
# ------------------------------------------------------
@app.route('/chat', methods=['POST'])
def chat_with_ai():
    global uploaded_pdf, pending_appointment, active_alert_context

    data = request.json
    user_msg = data.get("message", "")
    vitals = data.get("vitals", {})
    msg_lower = user_msg.lower()

    # STEP 0 — User giving appointment time
    if pending_appointment.get("awaiting_time"):
        doctor = pending_appointment["doctor"]
        appointment_time = user_msg.strip()
        pending_appointment.clear()
        log_activity(f"✔ Appointment booked with <b>{doctor['name']}</b> ({doctor['specialty']}) at <b>{appointment_time}</b>")
        return jsonify({
            "response": f"Done. I've scheduled you with **{doctor['name']}** for **{appointment_time}**. Take care.",
            "action": "none"
        })

    # STEP 1 — Explicit booking
    explicit_booking_phrases = ["book appointment", "book an appointment", "schedule appointment", "help me book"]
    if any(p in msg_lower for p in explicit_booking_phrases):
        doctor = pick_doctor(msg_lower)
        pending_appointment = {"doctor": doctor, "awaiting_time": True}
        return jsonify({
            "response": f"I think it would be best if you saw **{doctor['name']}** ({doctor['specialty']}). What time suits you best?",
            "action": "none"
        })

    # NORMAL CHAT
    chat = client.chats.create(
        model=MODEL_ID,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.7
        )
    )

    parts = []
    if uploaded_pdf and any(x in msg_lower for x in ["pdf", "report", "scan"]):
        parts.append(types.Part(file_data=types.FileData(file_uri=uploaded_pdf.uri, mime_type=uploaded_pdf.mime_type)))

    # ⭐ INJECT CONTEXT
    # This tells the AI: "You started this. The user is replying to your alert."
    context_text = f"Current Patient Vitals: {json.dumps(vitals)}\n"
    
    if active_alert_context:
        context_text += f"IMPORTANT CONTEXT: You (the doctor) just proactively asked the patient: '{active_alert_context}'.\n"
        context_text += f"The patient is now replying to that specific question.\n"
        # Reset context so it doesn't get stuck
        active_alert_context = None 

    context_text += f"Patient Reply: {user_msg}"

    parts.append(types.Part(text=context_text))

    try:
        response = chat.send_message(parts)
        reply = response.text
    except Exception as e:
        reply = f"I'm having a little trouble accessing my records. Could you repeat that?"

    return jsonify({"response": reply, "action": "none"})

if __name__ == "__main__":
    app.run(port=5000, debug=True)