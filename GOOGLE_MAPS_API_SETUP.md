# Google Maps API Key Setup Guide

## 🎯 Quick Steps to Get Your API Key

### **Step 1: Create/Login to Google Cloud Account**
1. Go to: https://console.cloud.google.com/
2. Sign in with your Google account (or create one)
3. Accept terms if prompted

---

### **Step 2: Create a New Project**
1. Click the project dropdown at the top (next to "Google Cloud")
2. Click **"New Project"**
3. Enter project name: `Trauma Detection System` (or any name)
4. Click **"Create"**
5. Wait a few seconds, then select your new project from the dropdown

---

### **Step 3: Enable Required APIs**
1. Go to **"APIs & Services"** → **"Library"** (in the left sidebar)
2. Search for **"Places API"** and click it
3. Click **"Enable"** button
4. Go back to Library
5. Search for **"Maps JavaScript API"** (optional, but recommended)
6. Click **"Enable"**

**Required APIs:**
- ✅ **Places API** (for finding hospitals)
- ✅ **Maps JavaScript API** (optional, for maps display)

---

### **Step 4: Create API Key**
1. Go to **"APIs & Services"** → **"Credentials"** (in the left sidebar)
2. Click **"+ CREATE CREDENTIALS"** at the top
3. Select **"API key"**
4. Your API key will be created and displayed
5. **Copy the API key** (you'll need it in Step 6)

---

### **Step 5: Restrict API Key (Recommended for Security)**
1. Click on your newly created API key to edit it
2. Under **"API restrictions"**, select **"Restrict key"**
3. Check only:
   - ✅ **Places API**
   - ✅ **Maps JavaScript API** (if you enabled it)
4. Under **"Application restrictions"**, you can:
   - Select **"HTTP referrers"** and add your domain (for web apps)
   - Or leave it **"None"** for testing
5. Click **"Save"**

---

### **Step 6: Add API Key to Your Project**
1. Open your `.env` file in `backend/src/.env`
2. Find the line: `GOOGLE_MAPS_API_KEY=`
3. Add your API key after the `=` sign:
   ```
   GOOGLE_MAPS_API_KEY=YOUR_API_KEY_HERE
   ```
4. **Example:**
   ```
   GOOGLE_MAPS_API_KEY=AIzaSyB1234567890abcdefghijklmnopqrstuvw
   ```
5. Save the file

---

### **Step 7: Verify It Works**
1. Run your system: `python run.py`
2. Check the logs - you should see:
   - `"Hitting Google Maps API → nearest trauma center"`
   - `"Found: [Hospital Name]"`
3. If you see hospital names from Google Maps, it's working! ✅

---

## 💰 Pricing Information

### **Free Tier (Free Credits)**
- Google provides **$200 free credits per month**
- Places API: **$17 per 1,000 requests** (after free tier)
- With free credits, you get **~11,000 requests/month free**

### **For Hackathon/Demo:**
- **Completely FREE** for small-scale testing
- Free credits are more than enough for demos
- No credit card required for free tier

### **If You Need More:**
- After free credits, you pay per request
- Very affordable for small projects
- Can set billing alerts to avoid surprises

---

## 🔒 Security Best Practices

1. **Restrict API Key** (as shown in Step 5)
   - Only enable APIs you need
   - Restrict to specific domains/IPs if possible

2. **Don't Commit API Key to Git**
   - Keep it in `.env` file (already in `.gitignore`)
   - Never share API key publicly

3. **Monitor Usage**
   - Go to **"APIs & Services"** → **"Dashboard"**
   - Check API usage regularly

---

## ❌ Common Issues

### **Issue 1: "API key not valid"**
- **Solution**: Make sure you copied the entire key (no spaces)
- Check that Places API is enabled

### **Issue 2: "This API project is not authorized"**
- **Solution**: Enable Places API in Step 3

### **Issue 3: "Billing not enabled"**
- **Solution**: 
  - Go to **"Billing"** in Google Cloud Console
  - Add a payment method (required even for free tier)
  - Don't worry - you won't be charged if you stay within free limits

### **Issue 4: "Quota exceeded"**
- **Solution**: You've used all free credits
- Wait until next month OR upgrade billing plan

---

## 📝 Quick Checklist

- [ ] Created Google Cloud account
- [ ] Created new project
- [ ] Enabled Places API
- [ ] Created API key
- [ ] Restricted API key (optional but recommended)
- [ ] Added API key to `.env` file
- [ ] Tested the system

---

## 🎯 Summary

1. **Go to**: https://console.cloud.google.com/
2. **Create project** → **Enable Places API** → **Create API key**
3. **Add to `.env`**: `GOOGLE_MAPS_API_KEY=your_key_here`
4. **Done!** System will now find real hospitals near NESCO Centre Goregaon

**Time required**: ~5-10 minutes
**Cost**: FREE (within free tier limits)

---

## 🔗 Useful Links

- **Google Cloud Console**: https://console.cloud.google.com/
- **Places API Documentation**: https://developers.google.com/maps/documentation/places/web-service
- **API Key Best Practices**: https://developers.google.com/maps/api-security-best-practices

