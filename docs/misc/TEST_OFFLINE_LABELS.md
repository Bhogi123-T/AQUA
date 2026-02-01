# Offline Mode - LIVE/OFFLINE Labels Test Guide

## What Changed
When you go **OFFLINE**, ALL "LIVE" indicators automatically change to "OFFLINE":
- ✅ Badges show 📡 OFFLINE instead of 🔴 LIVE
- ✅ Ticker shows "OFFLINE" instead of "LIVE"  
- ✅ All live data fetching stops
- ✅ Pulse animations change color to red (#ff0055)

When you go back **ONLINE**, ALL labels switch back to LIVE:
- ✅ Badges show 🔴 LIVE
- ✅ Ticker shows "LIVE"
- ✅ Green pulse animations resume
- ✅ Live data fetching resumes

---

## Testing Instructions

### Step 1: Start the App
```bash
cd c:\Users\bhoge\OneDrive\Documents\Desktop\AQUA
python app.py
```
Visit: `http://localhost:5000`

### Step 2: Observe ONLINE Mode
Check these should show **LIVE**:
- [ ] Top connection badge: "🌐 ONLINE" with green background
- [ ] Ticker at bottom: Shows "🔴 LIVE:" in green
- [ ] Index page: "LIVE" badge on location tracker
- [ ] Index page: "SENSORS ACTIVE" badge on water quality
- [ ] Market page: "🔴 LIVE TELEMETRY" badge at top
- [ ] Pulse dots: Blinking green animation
- [ ] All data is updating in real-time

### Step 3: Go Offline (DevTools Method)
1. Open DevTools: **F12**
2. Go to **Application → Service Workers**
3. Check "Offline" checkbox ✓
4. Wait 2 seconds for page to detect offline

### Step 4: Verify OFFLINE Mode Changes
Check these should now show **OFFLINE**:
- [ ] **Connection Badge**: Changed to red 📡 OFFLINE
- [ ] **Ticker Text**: Changed from "LIVE:" to "OFFLINE:"
- [ ] **Location Badge**: Changed to "📡 OFFLINE" (red)
- [ ] **Sensors Badge**: Changed to "📡 OFFLINE" (red)
- [ ] **Market Badge**: Changed to "📡 OFFLINE TELEMETRY" (red)
- [ ] **Pulse Dots**: Changed to red, no blinking animation
- [ ] **Live Data**: All API calls stopped (check Network tab)
- [ ] **Elements Hidden**: Live-only sections become semi-transparent

### Step 5: Verify No External API Calls
In DevTools **Network Tab**:
- [ ] Weather API (wttr.in) - NO REQUESTS
- [ ] Nominatim (location) - NO REQUESTS  
- [ ] Market API (/api/market_live) - NO REQUESTS
- [ ] Realtime API (/api/realtime) - NO REQUESTS
- [ ] Only Service Worker cached responses used

### Step 6: Verify Cached Data Still Works
- [ ] Offline predictions still work
- [ ] Previously loaded market data visible
- [ ] Location coordinates still show if already loaded
- [ ] Farm data remains displayed
- [ ] No console errors

### Step 7: Go Back Online
1. DevTools → Application → Service Workers
2. Uncheck "Offline" checkbox ✓

### Step 8: Verify ONLINE Mode Restored
Check these should be back to **LIVE**:
- [ ] Connection badge: "🌐 ONLINE" green
- [ ] Ticker: "🔴 LIVE:" in green
- [ ] All badges: Show "LIVE" or "SENSORS ACTIVE"
- [ ] Pulse dots: Green blinking animation
- [ ] Live data updating again
- [ ] External API calls resuming

---

## Visual Changes Summary

### Connection Badge (Top Right)
| State | Display | Color | Icon |
|-------|---------|-------|------|
| ONLINE | 🌐 ONLINE | Green (#00ff88) | Globe |
| OFFLINE | 📡 OFFLINE | Red (#ff0055) | Antenna |

### Location Tracker Badge
| State | Display | Background | Text Color |
|-------|---------|------------|-----------|
| ONLINE | 🔴 LIVE | Green (0.2) | #00ff88 |
| OFFLINE | 📡 OFFLINE | Red (0.2) | #ff0055 |

### Sensors Badge
| State | Display | Background | Text Color |
|-------|---------|------------|-----------|
| ONLINE | 🔴 SENSORS ACTIVE | Cyan (0.2) | #00d2ff |
| OFFLINE | 📡 OFFLINE | Red (0.2) | #ff0055 |

### Market Telemetry Badge
| State | Display | Background | Text Color |
|-------|---------|------------|-----------|
| ONLINE | 🔴 LIVE TELEMETRY | Cyan (0.2) | #00d2ff |
| OFFLINE | 📡 OFFLINE TELEMETRY | Red (0.2) | #ff0055 |

### Ticker Status
| State | Display | Color |
|-------|---------|-------|
| ONLINE | 🔴 LIVE: | Green (#00ff88) |
| OFFLINE | 📡 OFFLINE: | Red (#ff0055) |

### Pulse Animation
| State | Animation | Background | Opacity |
|-------|-----------|-----------|---------|
| ONLINE | Blinking (2s) | Green | 1.0 |
| OFFLINE | None (frozen) | Red | 0.3 |

---

## Key Code Changes

### Global Flag: `window.ALLOW_LIVE_DATA`
```javascript
// Prevents ALL external API calls when offline
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) return;
```

### Label Update Function
```javascript
function updateLiveOfflineLabels(isOnline) {
    // Updates all badges and indicators
    // Changes LIVE ↔️ OFFLINE based on connection
}
```

### Badge Attributes
```html
<div data-badge-type="realtime" class="live-pulse-badge">...</div>
<div data-badge-type="sensors" class="live-pulse-badge">...</div>
<div data-badge-type="market" class="live-pulse-badge">...</div>
```

### HTML Elements
- `#ticker-live-text` - Ticker status label
- `.live-pulse-badge` - All status badges
- `.live-pulse` - Blinking dots
- `.status-badge-text` - Status text spans

---

## Troubleshooting

### Badges not changing color?
1. Open Console (F12 → Console)
2. Type: `window.ALLOW_LIVE_DATA`
3. Should be `false` when offline, `true` when online

### Labels still showing LIVE when offline?
1. Hard refresh: **Ctrl+Shift+R**
2. Clear Service Worker cache: Settings → Delete all cookies/cache
3. Check if `updateLiveOfflineLabels()` is being called

### Ticker not updating?
1. Check ticker HTML has `id="ticker-live-text"`
2. Verify main.js is loaded: F12 → Network → main.js
3. Check console for errors

### Still seeing API calls offline?
1. Look in Network tab for failed requests
2. Check if `window.ALLOW_LIVE_DATA` check is present
3. Verify fetch() calls have the guard clause

---

## Browser Testing

### Chrome/Edge
- ✅ DevTools → Application → Service Workers → Offline
- ✅ Simulates complete offline mode

### Firefox  
- ✅ DevTools → Network → Offline
- ✅ Disables all network requests

### Mobile Safari
- Settings → Airplane Mode ON
- App automatically switches to offline

### Chrome Mobile
- Tap menu → More tools → Developer tools
- Network tab → Offline

---

## Performance Metrics

### Online Mode
- Weather API: 1-2 seconds (with timeout)
- Market updates: Every 5 seconds
- Location updates: Every 60 seconds
- Real-time sensor data: Continuous

### Offline Mode
- Zero external API calls
- Zero network requests (except cached assets)
- Instant label updates
- Reduced CPU usage (no polling)
- Battery efficient

---

## Expected Behavior

### When Going Offline
```
1. Browser detects offline event
2. window.ALLOW_LIVE_DATA = false
3. hideLiveDataSections() called
4. updateLiveOfflineLabels(false) called
5. All badges change to OFFLINE
6. Ticker updates to show OFFLINE
7. All live data fetching stops
8. Pulse animation turns red and stops
9. Notification shows: "📡 You are now offline - Cached data only"
```

### When Going Online
```
1. Browser detects online event
2. window.ALLOW_LIVE_DATA = true
3. showLiveDataSections() called
4. updateLiveOfflineLabels(true) called
5. All badges change back to LIVE
6. Ticker updates to show LIVE
7. Live data fetching resumes
8. Pulse animation turns green and blinks
9. Notification shows: "🌐 You are back online!"
```

---

**Status**: ✅ COMPLETE - Perfect offline/online label switching
**Last Updated**: January 26, 2026
**Test Date**: Run through entire checklist before deployment
