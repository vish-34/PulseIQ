# Twilio Setup Guide - Complete Walkthrough

This guide will help you set up Twilio for real phone calls and SMS in your trauma detection system.

---

## 📋 Step 1: Sign Up for Twilio Account

1. **Go to Twilio Website**
   - Visit: https://www.twilio.com/try-twilio
   - Click "Sign up" or "Get Started"

2. **Create Account**
   - Enter your email address
   - Create a password
   - Verify your email address

3. **Complete Account Setup**
   - Fill in your name and phone number
   - Verify your phone number (they'll send a verification code)
   - Choose your country (India)
   - Accept terms and conditions

---

## 🔑 Step 2: Get Your Twilio Credentials

Once logged in to Twilio Console:

1. **Go to Dashboard**
   - You'll see your Account SID and Auth Token on the main dashboard
   - **Account SID**: Starts with `AC...` (e.g., `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`)
   - **Auth Token**: Click "View" to reveal it (e.g., `your_auth_token_here`)

2. **Copy These Credentials**
   - Keep them safe - you'll need them for `.env` file

---

## 📱 Step 3: Get a Twilio Phone Number

1. **Navigate to Phone Numbers**
   - In Twilio Console, go to: **Phone Numbers** → **Manage** → **Buy a number**

2. **Choose Your Number**
   - **Country**: Select "India" (or your country)
   - **Capabilities**: 
     - ✅ Voice (for calls)
     - ✅ SMS (for text messages)
   - Click "Search"

3. **Purchase Number**
   - Select a number from the list
   - Click "Buy" (Twilio trial accounts get $15.50 free credit)
   - The number will be in format: `+91XXXXXXXXXX` (for India)

4. **Copy Your Phone Number**
   - Note down the full number with country code (e.g., `+911234567890`)

---

## 💰 Step 4: Understanding Twilio Trial Account

**Trial Account Limits:**
- ✅ $15.50 free credit
- ✅ Can make calls/SMS to **verified phone numbers only**
- ✅ Need to verify your phone number first

**To Verify Your Phone Number:**
1. Go to **Phone Numbers** → **Verified Caller IDs**
2. Click "Add a new Caller ID"
3. Enter your phone number (the one you want to receive calls/SMS)
4. Twilio will call/SMS you with a verification code
5. Enter the code to verify

**Important:** For hackathon demo, verify:
- Your family phone: `+917738187807`
- Your teammate's phone: `+918454030044`

---

## ⚙️ Step 5: Add Credentials to `.env` File

1. **Open your `.env` file**
   - Location: `backend/src/.env` (or copy from `info.env`)

2. **Add Twilio Credentials**
   ```env
   # Twilio Credentials
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=your_auth_token_here_do_not_commit_real_token
   TWILIO_PHONE_NUMBER=+911234567890
   
   # Family & Hospital Contacts (already in your info.env)
   FAMILY_PHONE=+917738187807
   FAMILY_EMAIL=rookiedev.mujahid@gmail.com
   HOSPITAL_PHONE=+918454030044
   HOSPITAL_EMAIL=vishal23borana@gmail.com
   ```

3. **Replace with Your Actual Values**
   - `TWILIO_ACCOUNT_SID`: Your Account SID from Step 2
   - `TWILIO_AUTH_TOKEN`: Your Auth Token from Step 2
   - `TWILIO_PHONE_NUMBER`: Your purchased Twilio number from Step 3

---

## 🧪 Step 6: Test Twilio Setup

1. **Copy `.env` to backend/src**
   ```powershell
   # From project root
   copy info.env backend\src\.env
   # Then edit backend\src\.env and add Twilio credentials
   ```

2. **Test the Setup**
   ```powershell
   python run.py
   ```

3. **What to Expect:**
   - When crash is confirmed → You'll receive:
     - 📞 **Phone call** to `+917738187807` (your family phone)
     - 📱 **SMS** to `+917738187807`
     - 📧 **Email** to `rookiedev.mujahid@gmail.com`
   
   - When hospital arrival → You'll receive:
     - 📞 **Phone call** to `+917738187807`
     - 📱 **SMS** to `+917738187807`
     - 📧 **Email** to `rookiedev.mujahid@gmail.com`

---

## 🚨 Troubleshooting

### Issue: "Trial account can only call verified numbers"
**Solution:**
- Verify your phone numbers in Twilio Console
- Go to **Phone Numbers** → **Verified Caller IDs**
- Add and verify `+917738187807` and `+918454030044`

### Issue: "Insufficient balance"
**Solution:**
- Trial account has $15.50 free credit
- For production, add payment method in Twilio Console
- Go to **Billing** → **Payment Methods**

### Issue: "Number not found"
**Solution:**
- Make sure `TWILIO_PHONE_NUMBER` includes country code
- Format: `+91XXXXXXXXXX` (not `91XXXXXXXXXX` or `0XXXXXXXXXX`)

### Issue: "Authentication failed"
**Solution:**
- Double-check `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN`
- Make sure there are no extra spaces in `.env` file
- Restart the server after updating `.env`

---

## 📊 Twilio Pricing (India)

**Voice Calls:**
- Outbound calls: ~₹0.50 per minute
- Trial credit: $15.50 ≈ ₹1,300 (good for ~2,600 minutes)

**SMS:**
- Outbound SMS: ~₹0.20 per message
- Trial credit: Good for ~6,500 SMS

**For Hackathon:**
- Trial account is usually sufficient
- Each demo run uses:
  - 2 calls (crash alert + hospital arrival) ≈ ₹1
  - 2 SMS ≈ ₹0.40
  - Total per demo: ~₹1.40

---

## ✅ Quick Checklist

- [ ] Signed up for Twilio account
- [ ] Got Account SID and Auth Token
- [ ] Purchased a Twilio phone number
- [ ] Verified your phone numbers (family + hospital)
- [ ] Added credentials to `backend/src/.env`
- [ ] Tested with `python run.py`
- [ ] Received test call and SMS

---

## 🎯 Next Steps After Setup

Once Twilio is configured, I will:
1. ✅ Add family notification (call + SMS + email) when crash is confirmed
2. ✅ Ensure hospital arrival triggers family notification (call + SMS + email)
3. ✅ Make sure all notifications use real Twilio when credentials are present
4. ✅ Test the complete flow end-to-end

**Ready to proceed once you've added Twilio credentials!**

---

## 📞 Need Help?

- **Twilio Support**: https://support.twilio.com
- **Twilio Docs**: https://www.twilio.com/docs
- **Twilio Console**: https://console.twilio.com

