# Fix Google Maps API - Step by Step

## ⚠️ Current Issue

The API is returning `REQUEST_DENIED`. This means one of these needs to be fixed:

---

## ✅ Step-by-Step Fix

### **Step 1: Verify Billing is Enabled**

1. Go to: **https://console.cloud.google.com/project/_/billing**
2. Make sure you see your project selected at the top
3. Check if billing account is linked:
   - If you see "Link a billing account" → Click it and add payment method
   - If you see a billing account name → Billing is enabled ✅

### **Step 2: Enable Places API**

1. Go to: **https://console.cloud.google.com/apis/library**
2. Make sure your project is selected (top dropdown)
3. Search for **"Places API"**
4. Click on **"Places API"**
5. Click **"Enable"** button
6. Wait a few seconds for it to enable

### **Step 3: Check API Key Restrictions**

1. Go to: **https://console.cloud.google.com/apis/credentials**
2. Click on your API key (the one in your .env file)
3. Under **"API restrictions"**:
   - Make sure **"Don't restrict key"** is selected, OR
   - If restricted, make sure **"Places API"** is checked
4. Under **"Application restrictions"**:
   - For testing, select **"None"**
   - Or add your IP/domain if you know it
5. Click **"Save"**

### **Step 4: Verify API Key is Correct**

1. In **https://console.cloud.google.com/apis/credentials**
2. Find your API key
3. Make sure it matches the one in `backend/src/.env`:
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyD07o-LoJW28gq70iwdnDo1WpLrMhENRoI
   ```
4. If different, copy the correct one to `.env`

### **Step 5: Test Again**

```powershell
python verify_google_maps_setup.py
```

You should see:
- ✅ `SUCCESS! Found X hospitals`
- ✅ List of real hospitals near NESCO Centre Goregaon

---

## 🔍 Common Issues

### **Issue 1: "Billing not enabled"**
- **Solution**: Even if you enabled it, make sure it's linked to THIS project
- Go to billing page and verify the project dropdown shows your project

### **Issue 2: "Places API not enabled"**
- **Solution**: Go to APIs Library and enable Places API
- Make sure it shows "Enabled" with a green checkmark

### **Issue 3: "API key restrictions"**
- **Solution**: Temporarily set restrictions to "None" for testing
- You can add restrictions later once it's working

### **Issue 4: "Wrong project"**
- **Solution**: Make sure the API key is from the project with billing enabled
- Check the project dropdown in Google Cloud Console

---

## ✅ Once It Works

After the API is working, the system will:
- ✅ Find real hospitals near NESCO Centre Goregaon
- ✅ Get real hospital names (e.g., "Kokilaben Dhirubhai Ambani Hospital")
- ✅ Get real addresses and GPS coordinates
- ✅ Calculate accurate distances
- ✅ Still use your configured phone/email for notifications

---

## 🧪 Quick Test

Run this to verify:
```powershell
python verify_google_maps_setup.py
```

Expected output:
```
SUCCESS! Found X hospitals
Nearest hospitals:
  1. [Real Hospital Name]
     Address: [Real Address]
```

---

## 📝 Checklist

- [ ] Billing enabled and linked to project
- [ ] Places API enabled
- [ ] API key restrictions allow Places API
- [ ] API key matches the one in .env
- [ ] Test script shows SUCCESS

---

## 🔗 Direct Links

- **Billing**: https://console.cloud.google.com/project/_/billing
- **APIs Library**: https://console.cloud.google.com/apis/library
- **Credentials**: https://console.cloud.google.com/apis/credentials

