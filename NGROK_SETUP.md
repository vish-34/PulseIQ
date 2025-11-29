# ngrok Setup Guide for Windows

## 🚀 Quick Installation

### **Option 1: Download ngrok (Recommended)**

1. **Download ngrok**:
   - Go to: https://ngrok.com/download
   - Download the Windows version (ZIP file)

2. **Extract the ZIP**:
   - Extract `ngrok.exe` to a folder (e.g., `C:\ngrok\`)

3. **Add to PATH** (Optional but recommended):
   - Press `Win + X` → System → Advanced system settings
   - Click "Environment Variables"
   - Under "System variables", find "Path" and click "Edit"
   - Click "New" and add: `C:\ngrok` (or wherever you extracted it)
   - Click "OK" on all windows
   - **Restart PowerShell** for changes to take effect

4. **Or use directly**:
   - Navigate to the folder where you extracted ngrok
   - Run: `.\ngrok.exe http 8000`

---

### **Option 2: Install via Chocolatey** (If you have Chocolatey)

```powershell
choco install ngrok
```

---

### **Option 3: Install via Scoop** (If you have Scoop)

```powershell
scoop install ngrok
```

---

## ✅ Verify Installation

After installation, verify it works:

```powershell
ngrok version
```

You should see the version number.

---

## 🔑 Sign Up for Free Account (Required)

1. **Sign up**: https://dashboard.ngrok.com/signup
2. **Get authtoken**: After signing up, go to: https://dashboard.ngrok.com/get-started/your-authtoken
3. **Configure ngrok**:
   ```powershell
   ngrok config add-authtoken YOUR_AUTH_TOKEN_HERE
   ```

---

## 🚀 Usage

### **Step 1: Start Your Server**
```powershell
cd C:\Users\Shayesta Shaikh\MHCC
python run.py
```

### **Step 2: In a NEW Terminal, Start ngrok**
```powershell
ngrok http 8000
```

**Output:**
```
ngrok                                                                              
                                                                                   
Session Status                online                                               
Account                       Your Name (Plan: Free)                               
Version                       3.x.x                                                
Region                        United States (us)                                   
Latency                       45ms                                                 
Web Interface                 http://127.0.0.1:4040                                
Forwarding                    https://abc123.ngrok.io -> http://localhost:8000    
                                                                                   
Connections                   ttl     opn     rt1     rt5     p50     p90         
                              0       0       0.00    0.00    0.00    0.00        
```

### **Step 3: Share the ngrok URL**
- Copy the `Forwarding` URL: `https://abc123.ngrok.io`
- Give this to your teammate for the frontend
- Frontend should call: `GET https://abc123.ngrok.io/api/trigger/crash`

---

## 📝 Quick Commands

```powershell
# Start ngrok (expose port 8000)
ngrok http 8000

# Start ngrok with custom domain (if you have one)
ngrok http 8000 --domain=your-domain.ngrok.io

# View ngrok web interface (shows all requests)
# Open in browser: http://127.0.0.1:4040
```

---

## ⚠️ Important Notes

1. **Keep ngrok running**: Don't close the ngrok terminal while testing
2. **URL changes**: Free ngrok URLs change each time you restart (unless you have a paid plan)
3. **Two terminals needed**:
   - Terminal 1: `python run.py` (your server)
   - Terminal 2: `ngrok http 8000` (tunnel)

---

## 🐛 Troubleshooting

### **Issue: "ngrok not recognized"**
- **Solution**: Add ngrok to PATH or use full path: `C:\ngrok\ngrok.exe http 8000`

### **Issue: "authtoken required"**
- **Solution**: Sign up and run: `ngrok config add-authtoken YOUR_TOKEN`

### **Issue: "port 8000 already in use"**
- **Solution**: Make sure your server is running on port 8000, or use different port:
  ```powershell
  ngrok http 8001  # If server is on 8001
  ```

---

## ✅ Summary

1. **Download ngrok** from https://ngrok.com/download
2. **Extract** to a folder (e.g., `C:\ngrok\`)
3. **Add to PATH** (optional) or use full path
4. **Sign up** at https://dashboard.ngrok.com/signup
5. **Configure**: `ngrok config add-authtoken YOUR_TOKEN`
6. **Use**: `ngrok http 8000`

Then your teammate can access your server via the ngrok URL!

