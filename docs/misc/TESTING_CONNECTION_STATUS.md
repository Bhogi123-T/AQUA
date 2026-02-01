# 🧪 Connection Status Testing Guide

## Quick Start Testing

### ✅ Test 1: See Online Status Badge (Takes 30 seconds)

**Step 1**: Open the app
```
1. Open http://localhost:5000 in your browser
2. Look at the LEFT SIDEBAR
```

**Step 2**: Find the connection badge
```
You should see:
   [Logo]
   🌐 ONLINE   (Green box)
   
   Navigation Menu
```

**Step 3**: Verify it's GREEN
- Green background box
- Green text "ONLINE"
- Green 🌐 icon

✅ **Result**: Badge showing online status ✓

---

### ✅ Test 2: See Live Farm Intelligence Data

**Step 1**: Go to homepage
```
http://localhost:5000
```

**Step 2**: Scroll down to find:
```
🛰️ Live Farm Intelligence
├─ Live Location Tracker
├─ Live Weather Update
├─ Aquaculture Zones
└─ Water Body Distance
```

**Step 3**: Verify it's visible
- Should display weather data
- Should show location
- Should show zones

✅ **Result**: Live data visible when online ✓

---

### ✅ Test 3: Go Offline and Watch It Change (Takes 1 minute)

**Step 1**: Open DevTools
```
Press F12 (Windows) or CMD+Option+I (Mac)
```

**Step 2**: Go to Application tab
```
Click on "Application" in DevTools header
```

**Step 3**: Find Service Workers
```
Left sidebar → Storage → Service Workers
```

**Step 4**: Check "Offline" box
```
Click checkbox next to "Offline"
✓ Offline
```

**Step 5**: Watch the app change
```
Browser: Should show offline notification
Badge: Should turn 📡 OFFLINE (Red)
Data: Live sections should fade/hide
Message: "OFFLINE MODE" appears in ticker
```

**Expected Results**:
- ✅ Badge turns RED
- ✅ Icon changes to 📡
- ✅ Text changes to "OFFLINE"
- ✅ Red glow effect
- ✅ Live data sections hidden
- ✅ Notification appears: "📡 You are now offline"

✅ **Result**: Offline status working ✓

---

### ✅ Test 4: Go Back Online

**Step 1**: Uncheck "Offline" box
```
DevTools → Service Workers
Uncheck: ✓ Offline
```

**Step 2**: Watch the app change back
```
Badge: Should turn 🌐 ONLINE (Green)
Data: Live sections should appear
Message: Notification "✅ You are back online!"
```

**Expected Results**:
- ✅ Badge turns GREEN
- ✅ Icon changes to 🌐
- ✅ Text changes to "ONLINE"
- ✅ Green glow effect
- ✅ Live data sections shown again
- ✅ Notification appears: "✅ You are back online!"

✅ **Result**: Back to online mode working ✓

---

## Visual Verification Checklist

### Connection Badge
```
□ Visible in left sidebar
□ Shows correct icon (🌐 or 📡)
□ Shows correct text (ONLINE or OFFLINE)
□ Colors are bright and clear
□ Has glowing effect
```

### Badge Colors
```
Online State:
□ Green background (rgba(0, 255, 136, 0.2))
□ Green text (#00ff88)
□ Green glow effect

Offline State:
□ Red background (rgba(255, 0, 85, 0.2))
□ Red text (#ff0055)
□ Red glow effect
```

### Live Data Visibility
```
When Online:
□ Farm Intelligence section visible
□ Location tracker visible
□ Weather data visible
□ Zone info visible

When Offline:
□ Farm Intelligence section hidden
□ Location tracker hidden
□ Weather data hidden
□ Zone info hidden
□ "OFFLINE MODE" message shown
```

### Notifications
```
Going Offline:
□ Notification appears
□ Message: "You are now offline"
□ Appears in top-right corner
□ Disappears after 4 seconds

Coming Online:
□ Notification appears
□ Message: "You are back online"
□ Appears in top-right corner
□ Disappears after 4 seconds
```

---

## Console Testing (Advanced)

### Check Connection Status in Console

**Step 1**: Open DevTools Console
```
F12 → Console tab
```

**Step 2**: Check current connection
```javascript
navigator.onLine
```

**Result**:
```
true    // Online
false   // Offline
```

### Check API Response

**Step 3**: Test backend connection endpoint
```javascript
fetch('/api/connection-status')
    .then(r => r.json())
    .then(console.table)
```

**Expected Result**:
```
online:    true
status:    "ONLINE"
message:   "Connected to internet"
timestamp: "2026-01-26T..."
```

### Manually Trigger Status Update

```javascript
// Force update connection status
initializeConnectionMonitor();
```

---

## Prediction Testing: Offline vs Online

### Test Offline Prediction

**Step 1**: Go offline (F12 Offline mode)

**Step 2**: Go to a prediction page
```
Example: /disease?lang=en
```

**Step 3**: Fill form with values
```
Temperature: 28
pH: 7.5
Dissolved Oxygen: 6.0
Salinity: 15
Turbidity: 3
Species: Rohu
Country: India
```

**Step 4**: Click Submit

**Expected Results**:
- ✅ Result appears instantly (<500ms)
- ✅ Shows "Offline Prediction"
- ✅ Data saved locally
- ✅ Can reload page and result persists

### Test Online Prediction

**Step 1**: Go back online (uncheck offline)

**Step 2**: Go to prediction page
```
Example: /disease?lang=en
```

**Step 3**: Fill form with same values

**Step 4**: Click Submit

**Expected Results**:
- ✅ Result appears after ~1 second
- ✅ Uses real ML model
- ✅ May differ from offline version
- ✅ Stored in server

---

## Performance Checklist

### Page Load Performance
```
□ Badge appears instantly
□ No lag when loading
□ Smooth transitions
□ Fast response time
```

### Connection Detection
```
□ Badge changes within 1 second of going offline
□ Badge changes within 1 second of going online
□ No false positives (never shows wrong status)
□ Doesn't affect page load time
```

### Battery/CPU Usage
```
□ Battery drain same as before
□ CPU not spiking
□ No excessive logging
□ Smooth animations (60fps)
```

---

## Mobile Testing (iPhone/Android)

### iOS Safari
```
1. Open http://your-ip:5000 in Safari
2. Look for badge in sidebar
3. Turn on Airplane mode
4. Badge should turn red
5. Turn off Airplane mode
6. Badge should turn green
```

### Android Chrome
```
1. Open http://your-ip:5000 in Chrome
2. Look for badge in sidebar
3. Turn on Airplane mode
4. Badge should turn red
5. Turn off Airplane mode
6. Badge should turn green
```

---

## Real WiFi Testing

### Test 1: Real WiFi Disconnect
```
1. Connected to WiFi → Badge ONLINE (Green)
2. Turn off WiFi router
3. Wait 2-3 seconds
4. Badge should be OFFLINE (Red)
5. Turn on WiFi router
6. Wait 2-3 seconds
7. Badge should be ONLINE (Green)
```

### Test 2: Network Switch
```
1. Connected to WiFi → Badge ONLINE
2. Switch to Mobile Hotspot
3. Badge should stay ONLINE
4. Disconnect hotspot
5. Badge should go OFFLINE
```

---

## Troubleshooting Tests

### If Badge Doesn't Change

**Test 1**: Check browser console
```
F12 → Console
```
Look for errors. Should see:
```
Connection monitor initialized
```

**Test 2**: Reload page
```
Press F5 or Ctrl+R
```

**Test 3**: Clear cache and reload
```
Ctrl+Shift+Delete → Clear cache
F5 to reload
```

### If Live Data Doesn't Hide

**Test 1**: Check if `data-live-only` attribute exists
```
F12 → Inspector
Find element with class "live" or "intelligence"
Check for data-live-only attribute
```

**Test 2**: Check CSS
```
F12 → Elements → Styles
Look for display: none
```

**Test 3**: Check JavaScript
```
F12 → Console
Type: hideLiveDataSections()
Should hide all live sections
```

### If Notifications Don't Appear

**Test 1**: Check notifications permission
```
Check browser allows notifications
```

**Test 2**: Check console for errors
```
F12 → Console
Go offline → Look for notification code
```

**Test 3**: Manually trigger notification
```
F12 → Console
showNotification('Test message', 'success')
```

---

## Test Results Log

Use this template to record your test results:

```
Date: __________
Browser: __________
OS: __________

Test 1 - Badge Visible: □ PASS □ FAIL
Test 2 - Live Data Visible: □ PASS □ FAIL
Test 3 - Badge Changes Online: □ PASS □ FAIL
Test 4 - Live Data Hidden Offline: □ PASS □ FAIL
Test 5 - Badge Changes Back Online: □ PASS □ FAIL
Test 6 - Notifications Work: □ PASS □ FAIL
Test 7 - Offline Predictions: □ PASS □ FAIL
Test 8 - Online Predictions: □ PASS □ FAIL

Overall Status: ✅ PASS / ❌ FAIL
Issues Found: __________
```

---

## Summary

After running these tests, you should verify:

✅ Connection badge shows correctly (online = green, offline = red)
✅ Live data hides when offline
✅ Live data shows when online
✅ Notifications appear when status changes
✅ Predictions work both offline and online
✅ Performance is smooth
✅ Mobile works correctly
✅ No console errors

**Expected Status**: All tests passing ✓

---

**Version**: 1.0 | **Date**: January 26, 2026 | **Status**: Ready to Test
