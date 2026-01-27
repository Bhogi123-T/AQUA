# 🎯 Offline Status - Visual Reference Guide

## Quick Visual Guide: Before & After

### 📍 Homepage Location Tracking

#### ✅ ONLINE (Normal State)
```
┌─────────────────────────────────────────┐
│ 📍 LOCATION TRACKING                    │
│ Status Badge: [REAL TIME] (green)       │
│                                          │
│ Location: Mumbai, Maharashtra           │
│ Coordinates: 19.0760° N, 72.8777° E    │
│ Distance to Farm: 2.4 km                │
└─────────────────────────────────────────┘
```

#### ❌ OFFLINE (With Offline Indicator)
```
┌─────────────────────────────────────────┐
│ 📍 LOCATION TRACKING                    │
│ Status Badge: [📡 OFFLINE] (RED)        │
│                                          │
│ Location: Mumbai, Maharashtra (Cached)  │
│ Coordinates: 19.0760° N, 72.8777° E 📡 │
│ Distance to Farm: -- 📡                 │
└─────────────────────────────────────────┘
```

---

### 🌊 Water Quality Sensors

#### ✅ ONLINE (Normal State)
```
╔════════════════════════════════════╗
║ WATER QUALITY SENSORS              ║
║ Status: [SENSORS ACTIVE] (green)   ║
╠════════════════════════════════════╣
║ Temperature:    28.5°C             ║
║ pH:             7.8                ║
║ Dissolved O₂:   6.2 mg/L          ║
║ Ammonia:        0.15 mg/L          ║
║ Salinity:       18 ppt             ║
║ Turbidity:      25 NTU             ║
╚════════════════════════════════════╝
```

#### ❌ OFFLINE (With Offline Indicator)
```
╔════════════════════════════════════╗
║ WATER QUALITY SENSORS              ║
║ Status: [📡 OFFLINE] (RED)         ║
╠════════════════════════════════════╣
║ Temperature:    -- 📡              ║
║ pH:             -- 📡              ║
║ Dissolved O₂:   -- 📡              ║
║ Ammonia:        -- 📡              ║
║ Salinity:       -- 📡              ║
║ Turbidity:      -- 📡              ║
╚════════════════════════════════════╝
```

---

### 💰 Market Prices

#### ✅ ONLINE (Normal State)
```
┌──────────────────────────────────────┐
│ 🔴 LIVE TELEMETRY                    │ (Green badge)
│                                      │
│ VANNAMEI SHRIMP                      │
│ Price: $12.50 / kg                   │
│ INR: ₹1,037.50 / kg                  │
│ Status: 🚀 TRENDING UP               │
│ ⏱️ Live Update: 14:32:45             │
└──────────────────────────────────────┘
```

#### ❌ OFFLINE (With Offline Indicator)
```
┌──────────────────────────────────────┐
│ 📡 OFFLINE                           │ (RED badge)
│                                      │
│ VANNAMEI SHRIMP                      │
│ Price: $12.50 / kg (last known)      │
│ INR: ₹1,037.50 / kg (last known)     │
│ Status: ⏸️ UPDATES PAUSED             │
│ ⏱️ Last Update: 14:25:30             │
└──────────────────────────────────────┘
```

---

### 📦 Order Tracking

#### ✅ ONLINE (Normal State)
```
┌────────────────────────────────────────┐
│ LIVE SATELLITE                         │ (Green badge)
│                                        │
│ ORDER #AQ-102                          │
│ Status: EN ROUTE (LIVE)                │
│                                        │
│ GPS: 16.42° N, 82.15° E               │
│ Distance Remaining: 145 km            │
│ ETA: 2 hours                          │
└────────────────────────────────────────┘
```

#### ❌ OFFLINE (With Offline Indicator)
```
┌────────────────────────────────────────┐
│ 📡 OFFLINE                             │ (RED badge)
│                                        │
│ ORDER #AQ-102                          │
│ Status: EN ROUTE (OFFLINE)             │
│                                        │
│ GPS: 16.42° N, 82.15° E (Cached) 📡  │
│ Distance Remaining: 145 km (cached)   │
│ ETA: 2 hours (last known)             │
└────────────────────────────────────────┘
```

---

### 🛰️ IoT Dashboard

#### ✅ ONLINE (Normal State)
```
╔═══════════════════════════════════════╗
║ ● SENSORS ONLINE                      ║ (Green)
╠═════════╦═════════╦═════════╦═════════╣
║ Temp    ║ pH      ║ DO      ║ Ammonia ║
║ 28.5°C  ║ 7.8    ║ 6.2 mg  ║ 0.15 mg ║
║ Optimal ║Balanced║ Optimal ║ Safe    ║
╠═════════╬═════════╬═════════╬═════════╣
║ Health  ║ FCR     ║ Crash%  ║ Salinity║
║ 92%     ║ 1.2    ║ 5%      ║ 18 ppt  ║
║ Strong  ║Efficient║No Threat║ Optimal ║
╚═════════╩═════════╩═════════╩═════════╝
```

#### ❌ OFFLINE (With Offline Indicator)
```
╔═══════════════════════════════════════╗
║ 📡 SENSORS OFFLINE                    ║ (RED)
╠═════════╦═════════╦═════════╦═════════╣
║ Temp    ║ pH      ║ DO      ║ Ammonia ║
║ -- 📡   ║ -- 📡   ║ -- 📡   ║ -- 📡   ║
║ 📡 OFF  ║ 📡 OFF  ║ 📡 OFF  ║ 📡 OFF  ║
╠═════════╬═════════╬═════════╬═════════╣
║ Health  ║ FCR     ║ Crash%  ║ Salinity║
║ -- 📡   ║ -- 📡   ║ -- 📡   ║ -- 📡   ║
║ 📡 OFF  ║ 📡 OFF  ║ 📡 OFF  ║ 📡 OFF  ║
╚═════════╩═════════╩═════════╩═════════╝
```

---

### 👨‍🌾 Farmer Dashboard

#### ✅ ONLINE (Normal State)
```
╔════════════════════════════════════════╗
║ FARMER HUB - REAL-TIME FARM COMMAND    ║
║ [LIVE TELEMETRY] ● CONNECTED          ║ (Green)
╠════════════════════════════════════════╣
║                                        ║
║ ┌──────────────────┐  ┌──────────────┐ ║
║ │ STOCK HEALTH     │  │ WATER QUALITY│ ║
║ │ 92%              │  │ 6.2 DO       │ ║
║ │ ● ONLINE         │  │ 7.8 pH       │ ║
║ └──────────────────┘  └──────────────┘ ║
║ ┌──────────────────┐  ┌──────────────┐ ║
║ │ RISK STATUS      │  │ AI INSIGHTS  │ ║
║ │ SECURE           │  │ Feed: 120g   │ ║
║ │ ● ACTIVE         │  │ Power: 5kWh  │ ║
║ └──────────────────┘  └──────────────┘ ║
╚════════════════════════════════════════╝
```

#### ❌ OFFLINE (With Offline Indicator)
```
╔════════════════════════════════════════╗
║ FARMER HUB - REAL-TIME FARM COMMAND    ║
║ [📡 OFFLINE DATA] 📡 OFFLINE          ║ (RED)
╠════════════════════════════════════════╣
║                                        ║
║ ┌──────────────────┐  ┌──────────────┐ ║
║ │ STOCK HEALTH     │  │ WATER QUALITY│ ║
║ │ --               │  │ -- 📡        │ ║
║ │ 📡 OFFLINE       │  │ -- 📡        │ ║
║ └──────────────────┘  └──────────────┘ ║
║ ┌──────────────────┐  ┌──────────────┐ ║
║ │ RISK STATUS      │  │ AI INSIGHTS  │ ║
║ │ --               │  │ -- 📡        │ ║
║ │ 📡 OFFLINE       │  │ -- 📡        │ ║
║ └──────────────────┘  └──────────────┘ ║
╚════════════════════════════════════════╝
```

---

## Color Reference

### Status Colors
```
┌─────────────────────────────────────┐
│ 🟢 ONLINE / ACTIVE                  │
│ Color: #00ff88 (Bright Green)       │
│ Text: "● ONLINE" / "● ACTIVE"       │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🔴 OFFLINE / INACTIVE               │
│ Color: #ff6b6b (Red)                │
│ Text: "📡 OFFLINE"                  │
│ Background: Red tint                │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🟠 WARNING / CRITICAL               │
│ Color: #ff0055 (Hot Pink)           │
│ Text: "⚠️ CRITICAL" / "🚨 ALERT"    │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│ 🟡 CACHED / LAST KNOWN              │
│ Color: #ffcc00 (Yellow)             │
│ Text: "📡 (Offline)" / "(cached)"   │
└─────────────────────────────────────┘
```

---

## Badge Evolution

### Example: Market Badge Transformation

```
Stage 1: ONLINE
┌─────────────────────────┐
│ 🔴 LIVE TELEMETRY       │
│ (Green pulse animation) │
│ Updates: Every 5 sec    │
└─────────────────────────┘
         ↓
    Network Lost
         ↓
Stage 2: DETECTING OFFLINE
┌─────────────────────────┐
│ 🔴 LIVE TELEMETRY       │
│ (Color changing...)     │
│ Updates: Slowing down   │
└─────────────────────────┘
         ↓
         < 1 second
         ↓
Stage 3: OFFLINE
┌─────────────────────────┐
│ 📡 OFFLINE              │
│ (Red, no animation)     │
│ Updates: PAUSED         │
└─────────────────────────┘
         ↓
    Network Restored
         ↓
Stage 4: BACK ONLINE
┌─────────────────────────┐
│ 🔴 LIVE TELEMETRY       │
│ (Returning to green)    │
│ Updates: Resuming...    │
└─────────────────────────┘
         ↓
Stage 5: FULL SYNC
┌─────────────────────────┐
│ 🔴 LIVE TELEMETRY       │
│ (Green, normal)         │
│ Updates: Every 5 sec    │
└─────────────────────────┘
```

---

## Sensor State Transitions

### Temperature Sensor Example

```
Timeline of Sensor Display During Connection Loss:

14:25:00 - ONLINE
├─ Value: 28.5°C
├─ Status: "Optimal" (green)
└─ Updates: Every 3 seconds

14:25:05 - CONNECTION LOST (User offline)
├─ Value: 28.5°C (last)
├─ Status: "Optimal" (dimming)
└─ Notification: "🌐 Going offline..."

14:25:10 - FULL OFFLINE
├─ Value: -- 📡 (frozen)
├─ Status: 📡 OFFLINE (red)
└─ Updates: STOPPED

14:30:00 - BACK ONLINE
├─ Value: 28.5°C (fetching new)
├─ Status: "Optimal" (green, loading)
└─ Updates: RESUME

14:30:05 - SYNC COMPLETE
├─ Value: 29.2°C (updated)
├─ Status: "Optimal" (green)
└─ Updates: Every 3 seconds (normal)
```

---

## Network Transition Flowchart

```
                    ┌─────────────┐
                    │   ONLINE    │
                    │  (Normal)   │
                    └──────┬──────┘
                           │
                    API Calls ✓
                    Updates ✓
                    Live Data ✓
                           │
            ┌──────────────┼──────────────┐
            │              │              │
        WiFi Off      Network Timeout   Connection Lost
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                  ┌────────────────┐
                  │ TRANSITION     │
                  │ (< 1 second)   │
                  └────────┬───────┘
                           ↓
                    ┌─────────────┐
                    │   OFFLINE   │
                    │   (Cached)  │
                    └──────┬──────┘
                           │
                    API Calls ✗
                    Updates ∧ (from cache)
                    Live Data ∧ (last known)
                           │
            ┌──────────────┼──────────────┐
            │              │              │
        WiFi On     Network Restored    Connection Regained
            │              │              │
            └──────────────┼──────────────┘
                           ↓
                  ┌────────────────┐
                  │ TRANSITION     │
                  │ (< 1 second)   │
                  └────────┬───────┘
                           ↓
                  API Calls Resume ✓
                  Cache Updates
                  UI Refresh
                           ↓
                    ┌─────────────┐
                    │   ONLINE    │
                    │  (Normal)   │
                    └─────────────┘
```

---

## Icon Reference

| Icon | Meaning | Color | Used For |
|------|---------|-------|----------|
| 🟢 ● | Online | Green | Active connection |
| 📡 | Offline | Red | No connection |
| 🌐 | Network | Blue | Internet status |
| ⚠️ | Warning | Orange | Alert status |
| 🚨 | Critical | Red | Urgent action |
| ⏱️ | Timer | Yellow | Time-related |
| 💾 | Cache | Gray | Cached data |
| 🔄 | Sync | Blue | Syncing data |
| ✓ | Success | Green | Confirmed |
| ✗ | Error | Red | Failed |

---

## Status String Reference

### What Users See

**Online:**
```
"● ONLINE"          (Green text)
"● CONNECTED"       (Green text)
"● ACTIVE"          (Green text)
"● SENSORS ONLINE"  (Green text)
"REAL TIME"         (Green badge)
"SENSORS ACTIVE"    (Green badge)
"LIVE SATELLITE"    (Green badge)
"LIVE TELEMETRY"    (Green badge)
```

**Offline:**
```
"📡 OFFLINE"        (Red text)
"📡 OFFLINE DATA"   (Red badge)
"📡 SENSORS OFFLINE"(Red badge)
"📡 OFFLINE"        (Red badge)
-- 📡               (Red values)
```

---

## Cached Data Indicators

```
When Cached Data Displayed:

Option 1: Direct Value
├─ Value: 28.5°C
└─ Notice: "📡 (Offline)" or "(cached)"

Option 2: With Emoji
├─ Value: 28.5°C 📡
└─ Status: Red color

Option 3: Fallback
├─ Value: -- 📡
└─ Meaning: No cache available

Option 4: With Timestamp
├─ Value: 28.5°C
├─ Source: "Last updated: 14:25"
└─ Status: 📡 OFFLINE
```

---

## Performance Indicators

```
Update Frequency:

ONLINE (Live Mode):
├─ Status badges: Every 1 second
├─ Sensor values: Every 3-5 seconds
├─ Location data: Every 60 seconds
└─ API calls: As scheduled

OFFLINE (Cached Mode):
├─ Status badges: Every 1 second
├─ Sensor values: Static (no updates)
├─ Location data: Last known
└─ API calls: NONE
```

---

## Summary

**🎯 Key Visual Principle:**
- **GREEN** = Live Data Flowing ✓
- **RED** = No Connection, Cached Data ✗
- **🎵 Pulse** = Actively updating
- **🔴 Static** = Frozen at last value
- **📡** = Offline indicator emoji

---

**Visual Design Status: ✅ COMPLETE**  
**User Experience: ✅ CONSISTENT**  
**Accessibility: ✅ CLEAR INDICATORS**

