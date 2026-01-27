# Complete Live Sensors Offline Indicator System

## Overview
All live sensors and real-time data displays now show "OFFLINE" status when the network connection is lost, providing clear visual indication across the entire app.

## Sensors & Live Data Covered

### Homepage (index.html)

#### 📍 **Live Location Tracker**
- **Online**: Shows real-time GPS coordinates, city name, weather
- **Offline**: "📡 OFFLINE - Cached data only", all values show "--"
- **Badge**: Changes from "REAL TIME" (green) to "📡 OFFLINE" (red)

#### 🌊 **Water Quality Sensors**
- **Online**: Real-time water parameters (Temp, pH, DO, Ammonia, Turbidity, Salinity)
- **Offline**: All values show "-- 📡", status shows "📡 OFFLINE"
- **Badge**: Changes from "SENSORS ACTIVE" (green) to "📡 OFFLINE" (red)

#### 🐠 **Biological Tracker**
- **Online**: Health %, FCR, Growth Rate, Days to Harvest
- **Offline**: All show "-- 📡"

#### ⚠️ **Risk Center**
- **Online**: Oxygen crash probability, disease risk %
- **Offline**: All show "-- 📡", status turns red

#### 💡 **AI Insights**
- **Online**: Next feed time, aerator count, power usage
- **Offline**: All show "-- 📡"

### Farmer Dashboard (farmer_hub.html)
- Stock Health: "92% 📡" (online) → "📡 OFFLINE" (offline)
- Knowledge Graph: "● ACTIVE" (online) → "📡 OFFLINE" (offline)

### Transport Tracking (order_tracker.html, logistics.html)
- GPS positions: Shows coordinates (online) → "📡 OFFLINE - Last Known Location" (offline)
- Shipping status: "EN ROUTE (LIVE)" (online) → "📡 OFFLINE" (offline)

### Other Pages with Live Data
- `iot_dashboard.html`: IoT sensor data → "📡 OFFLINE"
- `feed_calculation.html`: Live feed recommendations → "📡 OFFLINE"
- `disease_analysis.html`: Real-time disease risk → "📡 OFFLINE"
- `yield_forecast.html`: Live yield predictions → "📡 OFFLINE"

## Visual Changes

### Online State
```
Badge: "REAL TIME" / "SENSORS ACTIVE" (green, pulsing)
Values: Clean numbers (e.g., "28.5°C", "7.2 pH", "5.59 mg/L")
Status: "● ONLINE" / "● ACTIVE" (green)
Color: Normal vibrant colors
```

### Offline State
```
Badge: "📡 OFFLINE" (red, no pulse)
Values: With 📡 emoji (e.g., "28.5 📡", "-- 📡")
Status: "📡 OFFLINE" (red)
Color: Red/dimmed, opacity reduced
```

## Implementation Details

### Badge Updates in index.html
```html
<!-- Location badge -->
<div id="location-badge" class="live-pulse-badge">{{ trans['real_time'] }}</div>

<!-- Sensors badge -->
<div id="sensors-badge" class="live-pulse-badge">{{ trans['sensors_active'] }}</div>
```

### JavaScript Functions

#### updateLiveLocation()
```javascript
// Checks if online/ALLOW_LIVE_DATA
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) {
    // Updates location badge to red "📡 OFFLINE"
    // Sets all location fields to show offline message
    // Disables refresh button
}
```

#### updateAIStats()
```javascript
// Checks if online/ALLOW_LIVE_DATA
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) {
    // Calls showSensorsOffline()
    // Updates sensors badge to "📡 OFFLINE"
}

function showSensorsOffline() {
    // Sets all sensor values to "-- 📡"
    // Updates all status indicators to "📡 OFFLINE" (red)
    // Calls updateSensorsBadge()
}
```

### Event Listeners
```javascript
// When coming back online
window.addEventListener('online', () => {
    updateWeather();
    updateLiveLocation();
    updateAIStats();
    updateMarketPrices();
});

// When going offline
window.addEventListener('offline', () => {
    showSensorsOffline();
    // Update all badges to offline
});
```

## User Experience Flow

### Scenario: Network Goes Down While Viewing Sensors

```
Step 1: User viewing live sensors (ONLINE)
├─ Location Badge: "REAL TIME" (green, pulsing)
├─ Sensors Badge: "SENSORS ACTIVE" (green, pulsing)
├─ Location: "📍 Chennai, India" (live)
├─ Temperature: "28.5°C" (live)
├─ pH: "7.2" (live)
└─ DO: "5.59 mg/L" (live)

Step 2: Network disconnects (IMMEDIATE)
├─ Location Badge: "📡 OFFLINE" (red)
├─ Sensors Badge: "📡 OFFLINE" (red)
├─ Location: "📡 Offline - Cached data only"
├─ Temperature: "28.5 📡" (cached)
├─ pH: "7.2 📡" (cached)
├─ DO: "5.59 📡" (cached)
├─ All status indicators: "📡 OFFLINE" (red)
└─ No API calls made

Step 3: Network reconnects (AUTOMATIC)
├─ Location Badge: "REAL TIME" (green)
├─ Sensors Badge: "SENSORS ACTIVE" (green)
├─ Fresh sensor data fetched
├─ All values update without 📡 emoji
└─ Live updates resume
```

## Data Cached & Displayed Offline

✅ **Cached and shown with 📡 emoji:**
- Last known GPS coordinates
- Last sensor readings (temp, pH, DO, etc.)
- Previous health status
- Last AI insights
- Previous market data

❌ **Not available offline:**
- Real-time updates
- New predictions
- Live market changes
- Current GPS position
- Fresh AI analysis

## Badge Styling

### Online Badge
```css
.live-pulse-badge {
    background: (default pulsing animation);
    color: var(--primary) or var(--accent);
    border: 1px solid rgba(0, 255, 136, 0.2);
    animation: pulse 1.5s infinite;
}
```

### Offline Badge
```css
.live-pulse-badge.offline {
    background: rgba(255, 107, 107, 0.2);
    color: #ff6b6b;
    border: 1px solid #ff6b6b;
    animation: none;
}
```

## HTML/JS Elements Modified

| Element | ID | Location |
|---------|----|----|
| Location Badge | `location-badge` | index.html line ~37 |
| Sensors Badge | `sensors-badge` | index.html line ~120 |
| Location Name | `live-location-name` | index.html line ~60 |
| Temperature | `rt-temp` | index.html line ~150 |
| pH Level | `rt-ph` | index.html line ~160 |
| Dissolved Oxygen | `rt-do` | index.html line ~170 |
| Ammonia | `rt-ammonia` | index.html line ~180 |
| Turbidity | `rt-turbidity` | index.html line ~190 |
| Salinity | `rt-salinity` | index.html line ~200 |
| Health Index | `rt-health` | index.html line ~220 |

## Code Locations

| Component | File | Function |
|-----------|------|----------|
| Location offline logic | `index.html` | `updateLiveLocation()` |
| Sensors offline logic | `index.html` | `updateAIStats()` |
| Offline display | `index.html` | `showSensorsOffline()` |
| Online event handler | `index.html` | `window.addEventListener('online')` |
| Offline event handler | `index.html` | `window.addEventListener('offline')` |
| Location badge | `index.html` | ID: `location-badge` |
| Sensors badge | `index.html` | ID: `sensors-badge` |

## Testing Procedure

### Test 1: Go Offline While Viewing Sensors
```
1. Open http://localhost:5000
2. Wait for sensors to load and show live data
3. Open DevTools (F12) → Network tab
4. Check "Offline" checkbox
5. OBSERVE:
   ├─ Both badges change to red "📡 OFFLINE"
   ├─ All sensor values add 📡 emoji
   ├─ Status indicators turn red
   ├─ No new API calls made
   ├─ Existing data still visible (cached)
6. Uncheck "Offline" → Resumes live updates
```

### Test 2: Open Page While Offline
```
1. Disable WiFi
2. Open http://localhost:5000
3. Wait for page load
4. OBSERVE:
   ├─ Both badges show "📡 OFFLINE"
   ├─ All values show "--" or "-- 📡"
   ├─ Status shows offline messages
5. Enable WiFi
6. OBSERVE:
   ├─ Updates start immediately
   ├─ Badges turn green
   ├─ Fresh data loads
```

### Test 3: Mobile Network Transition
```
1. Open app on mobile with WiFi
2. Leave WiFi range (simulates slow network)
3. OBSERVE: Badges change to offline
4. Re-enter WiFi range
5. OBSERVE: Badges update back to online
```

## Global Offline State

All offline checks use the same global system:

```javascript
// Set in static/main.js
window.ALLOW_LIVE_DATA

// Checked everywhere
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) {
    // Show offline
}
```

This ensures **consistent offline indicators** across:
- ✅ All sensor data on homepage
- ✅ Farmer dashboard telemetry
- ✅ Transport tracking
- ✅ Market prices
- ✅ Weather updates
- ✅ All real-time features

## Performance Impact

- **Memory**: Minimal - just badge updates
- **Network**: Zero API calls when offline
- **Battery**: Saved by preventing failed requests
- **CPU**: Lightweight status updates
- **Updates**: Every 1 second for status checks

## Browser Compatibility

- ✅ Chrome/Chromium: Full support
- ✅ Firefox: Full support
- ✅ Safari: Full support
- ✅ Edge: Full support
- ✅ Mobile browsers: Full support
- ✅ Offline detection: Standard `navigator.onLine` API

## Future Enhancements

- [ ] Show "Syncing..." animation when reconnecting
- [ ] Timestamp of last update on each sensor
- [ ] Trending indicators (↑/↓) for cached values
- [ ] Historical data graphs when offline
- [ ] Notify user after X minutes offline
- [ ] Auto-refresh when back online
- [ ] Store more data points in IndexedDB

---

**Status**: ✅ COMPLETE - All live sensors show unified offline status
**Last Updated**: January 26, 2026
**Version**: 1.0
**Coverage**: Homepage + Dashboard + Tracking + All live features
