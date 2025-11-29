# Frontend Button Code - Working Implementation

## ✅ JavaScript Code for OnClick Button

### **Option 1: Simple Fetch (Recommended)**

```javascript
const triggerCrash = async () => {
  const friendURL = "https://YOUR_NGROK_URL/api/trigger/crash";
  
  try {
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "X-Trigger-Token": "CRASH_BUTTON",  // ← CRITICAL: Exact header name and value
        "Content-Type": "application/json"
      }
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    const data = await res.json();
    console.log("Crash triggered successfully:", data);
    alert("✅ Crash triggered! Incident ID: " + data.incident_id);
    
  } catch (err) {
    console.error("Error triggering crash:", err);
    alert("⚠️ Error: " + err.message);
  }
};
```

---

### **Option 2: With Loading State**

```javascript
const triggerCrash = async () => {
  const friendURL = "https://YOUR_NGROK_URL/api/trigger/crash";
  
  // Show loading state
  const button = document.querySelector('.crash-button'); // Adjust selector
  const originalText = button.textContent;
  button.textContent = "Triggering...";
  button.disabled = true;
  
  try {
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "X-Trigger-Token": "CRASH_BUTTON",
        "Content-Type": "application/json"
      }
    });
    
    if (!res.ok) {
      const errorText = await res.text();
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    const data = await res.json();
    console.log("Crash triggered:", data);
    
    // Show success
    button.textContent = "✅ Triggered!";
    alert("Crash simulation started! Incident ID: " + data.incident_id);
    
    // Reset button after 2 seconds
    setTimeout(() => {
      button.textContent = originalText;
      button.disabled = false;
    }, 2000);
    
  } catch (err) {
    console.error("Error:", err);
    alert("⚠️ Error: " + err.message);
    
    // Reset button on error
    button.textContent = originalText;
    button.disabled = false;
  }
};
```

---

### **Option 3: React Component Example**

```jsx
import { useState } from 'react';

function CrashButton() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  
  const triggerCrash = async () => {
    const friendURL = "https://YOUR_NGROK_URL/api/trigger/crash";
    
    setLoading(true);
    setError(null);
    
    try {
      const res = await fetch(friendURL, { 
        method: "GET",
        headers: {
          "X-Trigger-Token": "CRASH_BUTTON",
          "Content-Type": "application/json"
        }
      });
      
      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`HTTP ${res.status}: ${errorText}`);
      }
      
      const data = await res.json();
      console.log("Crash triggered:", data);
      alert("✅ Crash triggered! Incident ID: " + data.incident_id);
      
    } catch (err) {
      console.error("Error:", err);
      setError(err.message);
      alert("⚠️ Error: " + err.message);
    } finally {
      setLoading(false);
    }
  };
  
  return (
    <div>
      <button 
        onClick={triggerCrash} 
        disabled={loading}
        className="crash-button"
      >
        {loading ? "Triggering..." : "Trigger Crash"}
      </button>
      {error && <p style={{color: 'red'}}>Error: {error}</p>}
    </div>
  );
}

export default CrashButton;
```

---

## 🔑 Critical Points

### **1. Header Name (Case-Sensitive!)**
```javascript
"X-Trigger-Token": "CRASH_BUTTON"  // ✅ Correct
"x-trigger-token": "CRASH_BUTTON"  // ❌ Wrong (lowercase)
"X-Trigger-Token": "crash_button"  // ❌ Wrong (lowercase value)
```

### **2. Header Value (Exact Match!)**
```javascript
"X-Trigger-Token": "CRASH_BUTTON"  // ✅ Correct
"X-Trigger-Token": "Crash_Button"  // ❌ Wrong (different case)
"X-Trigger-Token": "CRASH BUTTON"  // ❌ Wrong (space instead of underscore)
```

### **3. Method**
```javascript
method: "GET"  // ✅ Must be GET
```

### **4. URL**
```javascript
// Replace YOUR_NGROK_URL with actual ngrok URL
const friendURL = "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash";
```

---

## 🚨 Common Mistakes

### **Mistake 1: Wrong Header Name**
```javascript
// ❌ WRONG
headers: {
  "x-trigger-token": "CRASH_BUTTON"  // lowercase won't work
}

// ✅ CORRECT
headers: {
  "X-Trigger-Token": "CRASH_BUTTON"  // exact case
}
```

### **Mistake 2: Wrong Header Value**
```javascript
// ❌ WRONG
headers: {
  "X-Trigger-Token": "crash_button"  // lowercase won't work
}

// ✅ CORRECT
headers: {
  "X-Trigger-Token": "CRASH_BUTTON"  // exact match
}
```

### **Mistake 3: Missing Header**
```javascript
// ❌ WRONG - No header
const res = await fetch(friendURL, { method: "GET" });

// ✅ CORRECT - With header
const res = await fetch(friendURL, { 
  method: "GET",
  headers: {
    "X-Trigger-Token": "CRASH_BUTTON"
  }
});
```

---

## 📝 Complete Example for Your Friend

**Copy this exact code:**

```javascript
const triggerCrash = async () => {
  // Replace with your actual ngrok URL
  const friendURL = "https://8d21e9398d8f.ngrok-free.app/api/trigger/crash";
  
  try {
    console.log("Sending crash trigger request...");
    
    const res = await fetch(friendURL, { 
      method: "GET",
      headers: {
        "X-Trigger-Token": "CRASH_BUTTON",
        "Content-Type": "application/json"
      }
    });
    
    console.log("Response status:", res.status);
    
    if (!res.ok) {
      const errorText = await res.text();
      console.error("Error response:", errorText);
      throw new Error(`HTTP ${res.status}: ${errorText}`);
    }
    
    const data = await res.json();
    console.log("✅ Crash triggered successfully:", data);
    alert("✅ Crash simulation started!\nIncident ID: " + data.incident_id);
    
  } catch (err) {
    console.error("❌ Error triggering crash:", err);
    alert("⚠️ Error: " + err.message);
  }
};
```

**Then use it in button:**
```jsx
<button onClick={triggerCrash}>Trigger Crash</button>
```

---

## ✅ Verification Checklist

Before testing, ensure:

- [ ] ngrok URL is correct (replace `YOUR_NGROK_URL`)
- [ ] Header name is exactly: `"X-Trigger-Token"`
- [ ] Header value is exactly: `"CRASH_BUTTON"`
- [ ] Method is `"GET"`
- [ ] URL ends with `/api/trigger/crash`
- [ ] Browser console is open to see logs

---

## 🔍 Debugging

**If it doesn't work:**

1. **Open browser DevTools (F12)**
2. **Go to Network tab**
3. **Click the crash button**
4. **Look for the GET request to `/api/trigger/crash`**
5. **Check:**
   - Is the request being sent?
   - Does it have the `X-Trigger-Token` header?
   - What's the response status?
   - Any CORS errors?

**Share the Network tab screenshot with your friend to debug!**

