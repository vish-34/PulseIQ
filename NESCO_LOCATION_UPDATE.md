# NESCO Centre Goregaon - Crash Location Update

## ✅ Changes Made

### **Updated Crash Location**
- **Location**: NESCO Centre Goregaon East, Mumbai
- **GPS Coordinates**: 
  - Latitude: `19.1680`
  - Longitude: `72.8500`

### **Files Updated**
1. **`backend/src/app.py`** (Line 84)
   - Updated test payload GPS coordinates to NESCO Centre location
   - System will now use this location for crash detection tests

2. **`backend/src/agents/core/crash_detector.py`** (Line 130)
   - Updated example documentation to reflect new location

---

## 🏥 Nearest Hospital Detection

The system will **automatically** find the nearest hospital to NESCO Centre Goregaon using:

1. **Google Maps Places API** (if `GOOGLE_MAPS_API_KEY` is configured)
   - Searches for hospitals within 10km radius
   - Prioritizes trauma centers and emergency facilities
   - Retrieves real hospital name, address, phone, and email

2. **Fallback to Configured Settings** (if Google Maps API not available)
   - Uses `HOSPITAL_PHONE` from `.env` (currently: `+918454030044`)
   - Uses `HOSPITAL_EMAIL` from `.env` (currently: `vishal23borana@gmail.com`)

---

## 📍 Expected Nearest Hospitals

Based on location, the system should find hospitals like:
- **Kokilaben Dhirubhai Ambani Hospital** (~2-3 km away)
- **Dr. Sabnis Hospital** (Naikwadi Road, Goregaon)
- **Kapadia Multi Speciality Hospital** (M.G. Road, Goregaon West)
- Other nearby hospitals in Goregaon area

---

## ✅ Credentials Preserved

All existing credentials remain **unchanged**:

- **Family Phone**: `+917738187807` (from `FAMILY_PHONE`)
- **Family Email**: `rookiedev.mujahid@gmail.com` (from `FAMILY_EMAIL`)
- **Hospital Phone**: `+918454030044` (from `HOSPITAL_PHONE` - used as fallback)
- **Hospital Email**: `vishal23borana@gmail.com` (from `HOSPITAL_EMAIL` - used as fallback)

**Note**: If Google Maps API finds a hospital, it will use the hospital's real phone/email. If not found, it falls back to your configured credentials.

---

## 🧪 Testing

When you run `python run.py`, the system will:
1. Use NESCO Centre Goregaon as crash location
2. Find nearest hospital via Google Maps API
3. Send notifications to your configured family/hospital contacts
4. Display the real hospital name and details in logs

---

## 📝 Summary

- ✅ Crash location updated to NESCO Centre Goregaon
- ✅ Nearest hospital will be found automatically
- ✅ All email/call credentials remain unchanged
- ✅ System ready to test with new location

