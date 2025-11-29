# SMTP Email Settings Guide

## 📧 Gmail SMTP Settings (Recommended - Free & Easy)

### Settings for `.env` file:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your.email@gmail.com
SMTP_PASSWORD=your_16_char_app_password
```

### Step-by-Step Setup:

1. **Get Gmail App Password:**
   - Go to: https://myaccount.google.com/apppasswords
   - Sign in with your Gmail account
   - Click "Select app" → Choose "Mail"
   - Click "Select device" → Choose "Other (Custom name)"
   - Type: `Trauma System`
   - Click "Generate"
   - **Copy the 16-character password** (remove spaces)

2. **Add to your `.env` file:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=your.email@gmail.com
   SMTP_PASSWORD=abcdefghijklmnop
   ```

3. **Example:**
   ```env
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=rookiedev.mujahid@gmail.com
   SMTP_PASSWORD=abcd efgh ijkl mnop
   ```
   (Remove spaces from password: `abcdefghijklmnop`)

---

## 📧 Other Email Providers

### Outlook/Hotmail:
```env
SMTP_HOST=smtp-mail.outlook.com
SMTP_PORT=587
SMTP_USER=your.email@outlook.com
SMTP_PASSWORD=your_password
```

### Yahoo Mail:
```env
SMTP_HOST=smtp.mail.yahoo.com
SMTP_PORT=587
SMTP_USER=your.email@yahoo.com
SMTP_PASSWORD=your_app_password
```

### Custom SMTP Server:
```env
SMTP_HOST=mail.yourdomain.com
SMTP_PORT=587
SMTP_USER=your.email@yourdomain.com
SMTP_PASSWORD=your_password
```

---

## ⚠️ Important Notes

1. **Gmail requires App Password** (not your regular password)
2. **Remove spaces** from the app password when adding to `.env`
3. **Port 587** is for TLS (recommended)
4. **Port 465** is for SSL (alternative)

---

## ✅ Quick Test

After adding SMTP settings to `.env`:
1. Restart the server
2. Run: `python run.py`
3. Check your configured email addresses for notifications!

