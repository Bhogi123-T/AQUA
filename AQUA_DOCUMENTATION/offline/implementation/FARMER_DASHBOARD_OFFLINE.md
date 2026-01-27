# Farmer Dashboard - Live Telemetry Offline Mode

## Overview
The Farmer Dashboard now intelligently detects when the app goes offline and seamlessly switches from live telemetry to cached data with clear offline indicators, preventing confusion about whether data is real-time or historical.

## What Changed

### Live Telemetry Badge
- **🟢 ONLINE**: Shows "LIVE TELEMETRY" badge in green with pulsing animation
- **🔴 OFFLINE**: Shows "📡 OFFLINE DATA" badge in red

### Connection Status Indicator
- **🟢 ONLINE**: Shows "● Connected" in green
- **🔴 OFFLINE**: Shows "📡 OFFLINE" in red

### Real-Time Data Display

#### When ONLINE:
```
Stock Health:    89% (live, updates every 3 seconds)
D.O.:            5.59 mg/L (live)
AMMONIA:         0.12 mg/L (live)
TEMP:            29.3°C (live)
pH:              8.1 (live)
```

#### When OFFLINE:
```
Stock Health:    89% 📡 (cached, frozen)
D.O.:            5.59 📡 (last known value)
AMMONIA:         0.12 📡 (last known value)
TEMP:            29.3 📡 (last known value)
pH:              8.1 📡 (last known value)
Risk:            OFFLINE - Last update: Cached data
```

## Technical Implementation

### Data Caching Strategy

```javascript
// When online - cache telemetry data
cachedFarmerData = data;
localStorage.setItem('cachedFarmerData', JSON.stringify(data));

// When offline - use cached data  
const cached = localStorage.getItem('cachedFarmerData');
if (cached) {
    // Display last known values
}
```

### Connection Detection

```javascript
// Check both network status AND global flag
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) {
    showOfflineDashboard();
    return;
}
```

### Status Badge Updates

The connection status and telemetry badges update automatically:
- **Online**: Green badge, live data updates every 3 seconds
- **Offline**: Red badge, frozen data with 📡 indicators
- **No Cache**: Shows dashes (--) with 📡 indicators

## User Experience Flow

### Scenario 1: Working Online → Goes Offline

```
Step 1: Working normally
├─ Live telemetry updating
├─ Badge: "LIVE TELEMETRY" (green)
├─ Status: "● Connected" (green)
└─ Data: Fresh updates every 3 seconds

Step 2: Network disconnects
├─ IMMEDIATE: Badge changes to "📡 OFFLINE DATA" (red)
├─ IMMEDIATE: Status changes to "📡 OFFLINE" (red)
├─ IMMEDIATE: Updates stop
└─ Data displayed with 📡 indicators showing cached

Step 3: User sees:
├─ Health: "89% 📡" (was live, now cached)
├─ DO: "5.59 📡" (was live, now cached)
├─ Ammonia: "0.12 📡" (was live, now cached)
└─ Risk: "OFFLINE - Last update: Cached data"
```

### Scenario 2: Opens Dashboard While Offline

```
Step 1: App loads while offline
├─ Checks localStorage for cached data
├─ Shows cached data if available
└─ Shows "NO DATA" if no cache

Step 2: Badge and status show:
├─ Badge: "📡 OFFLINE DATA" (red)
├─ Status: "📡 OFFLINE" (red)
└─ All data shows with 📡 indicators

Step 3: User reconnects
├─ IMMEDIATE: Live updates resume
├─ Badge changes back to "LIVE TELEMETRY" (green)
├─ Status changes back to "● Connected" (green)
└─ Data refreshes without 📡 indicators
```

## Visual Indicators

### Badge Styling

**Online State:**
```
[LIVE TELEMETRY] ← Green, pulsing animation
```

**Offline State:**
```
[📡 OFFLINE DATA] ← Red, no animation
```

### Status Text

**Online State:**
```
● Connected ← Green dot, says "connected"
```

**Offline State:**
```
📡 OFFLINE ← Red, clear offline indication
```

### Data Values

**Online:**
```
5.59 mg/L        ← Clean number only
```

**Offline:**
```
5.59 📡 mg/L     ← With 📡 satellite emoji to show cached
```

## Code Locations

| Component | File | Function |
|-----------|------|----------|
| Dashboard HTML | `templates/farmer_hub.html` | Badge ID: `telemetry-badge` |
| Status Indicator | `templates/farmer_hub.html` | Status ID: `connection-status` |
| Connection Logic | `templates/farmer_hub.html` | `updateConnectionStatus()` |
| Telemetry Update | `templates/farmer_hub.html` | `updateFarmerDashboard()` |
| Offline Fallback | `templates/farmer_hub.html` | `showOfflineDashboard()` |
| Event Listeners | `templates/farmer_hub.html` | `online/offline` events |
| Cache Storage | Browser localStorage | Key: `cachedFarmerData` |

## Real-Time Data Updates

### When ONLINE
- Updates every 3 seconds via `/api/realtime`
- AI advisor text updates with live analysis
- Risk levels recalculated dynamically
- Health bar animates smoothly
- All values fresh from server

### When OFFLINE
- No API calls made
- Updates stopped immediately
- Last known values displayed
- Health bar semi-transparent (opacity: 0.6)
- Risk shows "OFFLINE" status
- All values marked with 📡

## Testing Offline Telemetry

### Method 1: DevTools Offline Mode
```
1. Open Farmer Hub: http://localhost:5000/farmer
2. Open DevTools (F12)
3. Go to Network tab
4. Check "Offline" checkbox
5. Observe:
   ├─ Badge becomes red "📡 OFFLINE DATA"
   ├─ Status becomes "📡 OFFLINE"
   ├─ Values show with 📡 emoji
   └─ Updates stop immediately
```

### Method 2: Disable Network
```
1. Open Farmer Hub with data loaded
2. Turn off WiFi or disconnect ethernet
3. Observe immediate visual changes
4. Watch console for no fetch errors
5. Reconnect → Resumes live updates
```

### Method 3: Browser Offline Mode
```
1. Chrome: File → Work offline
2. Dashboard shows cached telemetry
3. No error messages in console
4. Uncheck "Work offline" → Updates resume
```

## Cache Management

### Data Cached
- Health Index (0-100%)
- Dissolved Oxygen (mg/L)
- Ammonia level (mg/L)
- Water Temperature (°C)
- pH Level
- Risk assessment
- All AI advisor text

### Cache Stored In
- Browser localStorage
- Key: `cachedFarmerData`
- Survives page refresh while offline
- Automatically updated when online

### Cache Lifespan
- Persists until new data downloaded
- Cleared/updated whenever online connection fetches new data
- Remains available indefinitely while offline

## What Doesn't Work Offline

❌ Live updates (frozen at last value)
❌ Real-time AI advisor changes
❌ Feed fraud detection updates
❌ Explainable AI endpoint calls
❌ New predictions or calculations

## What Still Works Offline

✅ View cached telemetry data
✅ See last known health metrics
✅ Understand water quality from cached values
✅ Access all other offline features
✅ Navigate to other pages
✅ View historical data from cache

## Performance Notes

- **Offline is more efficient**: No failed API timeouts
- **Battery savings**: Fewer network requests when offline
- **Smooth transitions**: No console spam or error messages
- **Instant feedback**: Badge/status updates immediately
- **Zero flicker**: Cached data displays without lag

## Troubleshooting

### Live data still showing when offline?
```
Check:
1. DevTools → Application → Service Workers
2. Verify "Offline" checkbox is checked
3. Check console: window.ALLOW_LIVE_DATA should be false
4. Verify navigator.onLine is false
```

### Badge not showing as offline?
```
Check:
1. window.ALLOW_LIVE_DATA value in console
2. navigator.onLine status
3. Browser console for JavaScript errors
4. Refresh the page (F5)
```

### No cached data showing?
```
Check:
1. DevTools → Application → localStorage
2. Look for "cachedFarmerData" key
3. Verify JSON is valid
4. Ensure you were online previously
```

### Updates resume too slowly?
```
Check:
1. Verify internet connection is active
2. Check /api/realtime endpoint responds
3. Refresh page to force immediate update
4. Look for console errors
```

## Integration with Global Offline System

The farmer dashboard uses the same global flag as all other features:

```javascript
// Set in static/main.js
window.ALLOW_LIVE_DATA

// Checked by farmer_hub.html
if (!navigator.onLine || !window.ALLOW_LIVE_DATA) {
    showOfflineDashboard();
}
```

This ensures **consistent offline behavior** across:
- Farmer dashboard telemetry (stops)
- Market prices (stops)
- Weather updates (stops)
- Transport tracking (stops)
- Cached data (still available)

## Files Modified

1. **templates/farmer_hub.html**
   - Added ID to telemetry badge: `id="telemetry-badge"`
   - Added `updateConnectionStatus()` function
   - Enhanced `updateFarmerDashboard()` with offline checks
   - Added `showOfflineDashboard()` fallback
   - Added online/offline event listeners
   - Added status update loop (every 1 second)
   - Added localStorage caching

## CSS Classes Used

- `.live-pulse-badge` - Green pulsing badge for online
- Red styling applied inline for offline state
- Opacity 0.6 on health bar when offline

## Future Enhancements

- [ ] Show timestamp of last update
- [ ] Trending indicators (↑ ↓) for cached values
- [ ] Sync cached data when back online
- [ ] Historical telemetry graphs
- [ ] Alert if offline for more than X minutes
- [ ] Automatically refresh when connection resumes

---

**Status**: ✅ COMPLETE - Farmer telemetry now clearly shows offline state
**Last Updated**: January 26, 2026
**Version**: 1.0
