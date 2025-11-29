# Enable Billing for Google Maps API

## ⚠️ Current Issue

The Google Maps API is returning `REQUEST_DENIED` because **billing is not enabled** on your Google Cloud project.

**Don't worry!** Even though billing needs to be enabled, you won't be charged if you stay within the free tier limits.

---

## ✅ Quick Fix (2 minutes)

### **Step 1: Enable Billing**
1. Go to: **https://console.cloud.google.com/project/_/billing/enable**
2. Select your project (the one where you created the API key)
3. Click **"Link a billing account"**
4. If you don't have a billing account:
   - Click **"Create billing account"**
   - Fill in your details (name, address, payment method)
   - **Note**: You won't be charged unless you exceed free limits

### **Step 2: Verify**
1. Go back to: **https://console.cloud.google.com/apis/credentials**
2. Make sure your API key is still there
3. Run the test again: `python test_hospital_finder.py`

---

## 💰 Free Tier Information

### **What You Get FREE:**
- **$200 free credits per month**
- **Places API**: $17 per 1,000 requests
- **With free credits**: ~11,000 requests/month **FREE**

### **For Hackathon/Demo:**
- **Completely FREE** for small-scale testing
- Free credits are more than enough
- You'll likely use < 100 requests for the entire demo

### **Billing Alerts:**
- Google will send you alerts if you approach limits
- You can set custom spending limits
- Can disable APIs anytime

---

## 🔒 Why Billing is Required

Even though it's free, Google requires billing to be enabled because:
1. **Prevents abuse** of free tier
2. **Allows monitoring** of API usage
3. **Enables automatic scaling** if needed

**You won't be charged** unless you:
- Exceed $200/month in API usage
- Explicitly upgrade to a paid plan

---

## ✅ After Enabling Billing

Once billing is enabled:
1. ✅ Google Maps API will work
2. ✅ System will find real hospitals near NESCO Centre Goregaon
3. ✅ Hospital names, addresses, GPS will be real
4. ✅ Still uses your configured phone/email for notifications

---

## 🧪 Test After Enabling

```powershell
python test_hospital_finder.py
```

You should see:
- ✅ Real hospital name (e.g., "Kokilaben Dhirubhai Ambani Hospital")
- ✅ Real address
- ✅ Real GPS coordinates
- ✅ Distance calculation

---

## 📝 Summary

1. **Enable billing**: https://console.cloud.google.com/project/_/billing/enable
2. **Add payment method** (required, but won't be charged)
3. **Test again**: `python test_hospital_finder.py`
4. **Done!** System will find real hospitals

**Time required**: ~2 minutes
**Cost**: FREE (within $200/month free tier)

---

## 🔗 Direct Links

- **Enable Billing**: https://console.cloud.google.com/project/_/billing/enable
- **Check API Usage**: https://console.cloud.google.com/apis/dashboard
- **API Credentials**: https://console.cloud.google.com/apis/credentials

