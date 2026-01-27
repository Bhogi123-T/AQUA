# Farmer Dashboard - Complete Offline Status Display

## Overview
The Farmer Dashboard now shows complete offline/online status indicators across ALL sections including Stock Health and Knowledge Graph, providing a unified offline experience where users immediately understand what is live and what is cached.

## Status Indicators

### Main Dashboard Badge
- **🟢 ONLINE**: "LIVE TELEMETRY" (green, pulsing)
- **🔴 OFFLINE**: "📡 OFFLINE DATA" (red)

### Connection Status
- **🟢 ONLINE**: "● Connected" (green)
- **🔴 OFFLINE**: "📡 OFFLINE" (red)

### Stock Health Section
- **🟢 ONLINE**: "● ONLINE" (green, full opacity)
- **🔴 OFFLINE**: "📡 OFFLINE" (red, 70% opacity)

### Knowledge Graph Section
- **🟢 ONLINE**: "● ACTIVE" (cyan, full opacity)
- **🔴 OFFLINE**: "📡 OFFLINE" (red, 70% opacity)

### Real-Time Data Values
- **🟢 ONLINE**: Clean values (e.g., "92%", "5.59 mg/L")
- **🔴 OFFLINE**: Values with 📡 emoji (e.g., "92% 📡", "5.59 📡")

## What Shows When ONLINE

```
┌─────────────────────────────────────────┐
│  [LIVE TELEMETRY] ● Connected           │
├─────────────────────────────────────────┤
│                                         │
│  STOCK HEALTH          WATER QUALITY    │
│  92% (live)            D.O.: 5.59       │
│  ═══════════════       AMMONIA: 0.12    │
│  ● ONLINE              TEMP: 29.3°C pH: 8.1
│                                         │
│  ALERTS & RISK         KNOWLEDGE GRAPH  │
│  SECURE                ● ACTIVE         │
│  (live analysis)       Synced data      │
│                                         │
└─────────────────────────────────────────┘
```

## What Shows When OFFLINE

```
┌─────────────────────────────────────────┐
│  [📡 OFFLINE DATA] 📡 OFFLINE           │
├─────────────────────────────────────────┤
│                                         │
│  STOCK HEALTH          WATER QUALITY    │
│  92% 📡 (cached)       D.O.: 5.59 📡    │
│  ═══════════════       AMMONIA: 0.12 📡 │
│  📡 OFFLINE            TEMP: 29.3 📡    │
│                        pH: 8.1 📡       │
│  ALERTS & RISK         KNOWLEDGE GRAPH  │
│  OFFLINE               📡 OFFLINE       │
│  (Last: Cached data)   (No live sync)   │
│                                         │
└─────────────────────────────────────────┘
```

## Visual Changes

### Online State
- ✅ Stock Health: Green border, full opacity
- ✅ Knowledge Graph: Primary color, full opacity
- ✅ Status badges: Green indicators
- ✅ Data values: Clean numbers
- ✅ Updates: Every 3 seconds

### Offline State
- ❌ Stock Health: Semi-transparent (70%), "📡 OFFLINE"
- ❌ Knowledge Graph: Semi-transparent (70%), "📡 OFFLINE"
- ❌ Status badges: Red indicators
- ❌ Data values: With 📡 emoji
- ❌ Updates: Stopped, frozen

## HTML Structure Changes

### Stock Health Section
```html
<div id="health-card">
    <p>STOCK HEALTH</p>
    <div id="live-health">92%</div>
    <div id="health-status">● ONLINE</div>  <!-- NEW -->
</div>
```

### Knowledge Graph Section
```html
<div id="knowledge-card">
    <p>🌍 KNOWLEDGE GRAPH</p>
    <div id="knowledge-status">● ACTIVE</div>  <!-- NEW -->
    <p id="knowledge-desc">Synced data</p>
</div>
```

## JavaScript Functions

### updateConnectionStatus()
```javascript
// Updates ALL status indicators simultaneously
// Checks: navigator.onLine && window.ALLOW_LIVE_DATA
// Updates:
//   - connection-status badge
//   - telemetry-badge
//   - health-status
//   - knowledge-status
//   - Card opacity levels
```

### showOfflineDashboard()
```javascript
// Called when offline
// Sets all indicators to OFFLINE state
// Loads cached data if available
// Updates health and knowledge status to "📡 OFFLINE"
```

## Automatic State Management

### Status Updates Every 1 Second
```javascript
setInterval(updateConnectionStatus, 1000);
```

### Live Data Updates Every 3 Seconds (Only if Online)
```javascript
setInterval(() => {
    if (navigator.onLine && window.ALLOW_LIVE_DATA) {
        updateFarmerDashboard();
    }
}, 3000);
```

### Event Listeners
```javascript
window.addEventListener('online', updateFarmerDashboard);
window.addEventListener('offline', showOfflineDashboard);
```

## Testing Complete Offline Flow

### Test 1: Go Online → Offline → Online

```
Step 1: Page loads (ONLINE)
├─ All badges show green
├─ "● ONLINE", "● ACTIVE" text
├─ Data updates every 3 seconds
└─ Stock Health and Knowledge Graph at full opacity

Step 2: Disable network (OFFLINE)
├─ ALL status indicators become red
├─ "📡 OFFLINE" appears everywhere
├─ Stock Health opacity → 70%
├─ Knowledge Graph opacity → 70%
├─ Data values get 📡 emoji
├─ Updates stop immediately
└─ No API calls made

Step 3: Re-enable network (BACK ONLINE)
├─ ALL status indicators become green again
├─ "● ONLINE", "● ACTIVE" text returns
├─ Opacity back to 100%
├─ 📡 emoji removed from values
├─ Updates resume every 3 seconds
└─ New data fetched immediately
```

### Test 2: Open Dashboard While Offline

```
Step 1: App loads offline
├─ Check localStorage for cachedFarmerData
├─ All badges show red
├─ "📡 OFFLINE" everywhere
└─ Shows cached data if available

Step 2: User connects
├─ updateConnectionStatus() runs every second
├─ Detects navigator.onLine = true
├─ Everything becomes green
└─ Live updates begin
```

## CSS Changes

### Semi-Transparent Offline Cards
```css
#health-card {
    opacity: 1;  /* online */
}

/* When offline */
#health-card {
    opacity: 0.7;  /* visually dimmed */
}
```

### Color Changes
```
Online:   var(--accent), var(--primary), #00ff88
Offline:  #ff6b6b (red), dimmed opacity
```

## Code Locations

| Component | File | Element ID |
|-----------|------|------------|
| Stock Health Card | `farmer_hub.html` | `health-card` |
| Health Status | `farmer_hub.html` | `health-status` |
| Knowledge Card | `farmer_hub.html` | `knowledge-card` |
| Knowledge Status | `farmer_hub.html` | `knowledge-status` |
| Main Badge | `farmer_hub.html` | `telemetry-badge` |
| Connection Status | `farmer_hub.html` | `connection-status` |
| Update Function | `farmer_hub.html` | `updateConnectionStatus()` |
| Offline Handler | `farmer_hub.html` | `showOfflineDashboard()` |

## User Experience Benefits

✅ **Unified Offline Message**: User sees "📡 OFFLINE" consistently across all sections
✅ **No Confusion**: Clear visual difference between online and offline states
✅ **Immediate Feedback**: Status changes appear within 1 second of network change
✅ **Smart Degradation**: Opacity change indicates "use with caution" (cached data)
✅ **Consistent Design**: Same pattern used everywhere (badges, status, data)
✅ **Professional Look**: Red/green indicators match industry standards
✅ **Performance**: Only updates every 1 second, not on every check

## What Gets Cached

- Health Index (0-100%)
- All water quality parameters
- Risk assessment state
- AI advisor recommendations
- Fraud detection status

## What Doesn't Cache

- Real-time price updates
- Feed fraud detection (requires fresh data)
- Explainable AI reasons
- New AI advisor recommendations

## Integration with Global System

```javascript
// Global flag from static/main.js
window.ALLOW_LIVE_DATA

// All checks use both:
if (!navigator.onLine || !window.ALLOW_LIVE_DATA)
```

This ensures consistent offline behavior across:
- Farmer Dashboard ✅
- Transport Tracking ✅
- Market Data ✅
- Weather Data ✅
- All live features ✅

## Future Enhancements

- [ ] Show timestamp of last update on each section
- [ ] Add sync animation when back online
- [ ] Show "Syncing..." state during data refresh
- [ ] Remember user preference for data freshness
- [ ] Add notification when back online
- [ ] Show estimated time for network recovery

---

**Status**: ✅ COMPLETE - All dashboard sections now show unified offline status
**Last Updated**: January 26, 2026
**Version**: 2.0
