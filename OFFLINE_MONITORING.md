# Offline Status & Monitoring Dashboard

## Real-Time Offline Monitoring

The AquaSphere app includes a comprehensive offline status dashboard at `/offline-status` that shows:

1. **Current Connection Status** (Real-time badge)
2. **Cached Datasets** (Available for offline use)
3. **Synced Predictions** (History of offline predictions)
4. **Storage Usage** (IndexedDB size and limits)
5. **Sync Status** (Last sync time, pending items)

---

## Accessing Offline Status

### In Browser
1. Go to: `http://localhost:5000/offline-status`
2. View real-time status dashboard
3. Check cached datasets
4. View synced prediction history

### In Mobile App
1. After installing as PWA/Native app
2. Navigate to `/offline-status`
3. Same dashboard available offline

---

## HTML Offline Indicator Component

Add this to any template to show real-time offline status:

```html
<!-- Offline Status Indicator -->
<div id="offline-indicator" class="offline-status">
    <span id="connection-status" class="status-badge online">🌐 Online</span>
    <span id="sync-status" class="status-info"></span>
</div>

<style>
    .offline-status {
        position: fixed;
        top: 20px;
        right: 20px;
        display: flex;
        gap: 10px;
        align-items: center;
        font-size: 14px;
        z-index: 1000;
    }

    .status-badge {
        padding: 8px 12px;
        border-radius: 20px;
        font-weight: bold;
        transition: all 0.3s ease;
    }

    .status-badge.online {
        background: #32CD32;
        color: white;
    }

    .status-badge.offline {
        background: #FF6347;
        color: white;
        animation: pulse 1s infinite;
    }

    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.6; }
    }

    .status-info {
        background: rgba(0, 0, 0, 0.7);
        color: white;
        padding: 6px 10px;
        border-radius: 5px;
        font-size: 12px;
    }
</style>

<script>
    // Initialize offline status indicator
    function initOfflineIndicator() {
        const statusBadge = document.getElementById('connection-status');
        const syncInfo = document.getElementById('sync-status');

        function updateStatus() {
            if (navigator.onLine) {
                statusBadge.textContent = '🌐 Online';
                statusBadge.className = 'status-badge online';
            } else {
                statusBadge.textContent = '📡 Offline';
                statusBadge.className = 'status-badge offline';
            }
        }

        // Update on page load
        updateStatus();

        // Update on connection change
        window.addEventListener('online', updateStatus);
        window.addEventListener('offline', updateStatus);

        // Show sync status
        if (window.offlineManager) {
            offlineManager.getFromIndexedDB('predictions').then(preds => {
                const unsynced = preds.filter(p => !p.synced).length;
                if (unsynced > 0) {
                    syncInfo.textContent = `${unsynced} pending`;
                    syncInfo.style.display = 'inline-block';
                }
            });
        }
    }

    document.addEventListener('DOMContentLoaded', initOfflineIndicator);
</script>
```

---

## Monitoring Offline Predictions

### View Pending Predictions (Frontend)

```javascript
// In browser console:
const pending = await offlineManager.getFromIndexedDB('predictions');
const unsyncedOnly = pending.filter(p => !p.synced);

console.table(unsyncedOnly.map(p => ({
    type: p.type,
    input: JSON.stringify(p.input),
    timestamp: new Date(p.timestamp).toLocaleString(),
    synced: p.synced
})));
```

### View All Synced Predictions (Server)

**API Endpoint**: `GET /offline-status`

Returns HTML dashboard with:
- All cached datasets
- All synced predictions
- Storage metrics

**JSON API**: `GET /offline-predictions.json` (if available)

```bash
curl http://localhost:5000/offline-predictions.json | python -m json.tool
```

---

## Storage Metrics

### Check IndexedDB Usage

```javascript
// In browser console:
async function checkStorageUsage() {
    if (navigator.storage && navigator.storage.estimate) {
        const {usage, quota} = await navigator.storage.estimate();
        const percentUsed = (usage / quota * 100).toFixed(2);
        
        console.log(`
            Storage Used: ${(usage / 1024 / 1024).toFixed(2)} MB
            Storage Quota: ${(quota / 1024 / 1024).toFixed(2)} MB
            Percentage: ${percentUsed}%
        `);
    }
}

checkStorageUsage();
```

### Dataset Sizes

| Dataset | Typical Size | Records |
|---------|--------------|---------|
| disease | 450 KB | 1000+ |
| location | 280 KB | 800+ |
| feed | 320 KB | 900+ |
| yield | 290 KB | 850+ |
| buyer | 240 KB | 600+ |
| stocking | 310 KB | 880+ |
| seed | 270 KB | 750+ |
| **Total** | **~2.4 MB** | **~6,500** |

**Available quota per origin**: 50MB (Chrome) - 1GB (depending on device storage)

---

## Sync Events & Logging

### Auto-Sync Triggers

Automatic sync happens when:
1. User goes back online
2. App is loaded/refreshed
3. User manually opens `/offline-status`
4. Service Worker detects connection
5. Every 30 minutes (if background sync enabled)

### Manual Trigger Sync

```javascript
// Manually trigger sync:
if (window.offlineManager) {
    offlineManager.syncPendingData().then(() => {
        console.log('✅ Sync complete!');
    }).catch(err => {
        console.error('❌ Sync failed:', err);
    });
}
```

### Monitoring Sync Process

```javascript
// Track sync progress
async function monitorSync() {
    const predictions = await offlineManager.getFromIndexedDB('predictions');
    
    setInterval(async () => {
        const updated = await offlineManager.getFromIndexedDB('predictions');
        const synced = updated.filter(p => p.synced).length;
        const total = updated.length;
        
        console.log(`Sync Progress: ${synced}/${total} (${(synced/total*100).toFixed(0)}%)`);
    }, 1000);
}
```

---

## Network Status Monitoring

### Real-Time Connection Monitor

```javascript
class ConnectionMonitor {
    constructor() {
        this.isOnline = navigator.onLine;
        this.setupListeners();
        this.logStatus();
    }

    setupListeners() {
        window.addEventListener('online', () => this.onOnline());
        window.addEventListener('offline', () => this.onOffline());
    }

    onOnline() {
        this.isOnline = true;
        console.log('🌐 Connected!', new Date().toLocaleTimeString());
        this.notifyUI('Connected', 'success');
    }

    onOffline() {
        this.isOnline = false;
        console.log('📡 Disconnected!', new Date().toLocaleTimeString());
        this.notifyUI('Offline Mode', 'warning');
    }

    logStatus() {
        const timestamp = new Date().toLocaleTimeString();
        const status = this.isOnline ? '🌐 Online' : '📡 Offline';
        console.log(`[${timestamp}] ${status}`);
    }

    notifyUI(message, type) {
        // Update UI badge or notification
        const badge = document.getElementById('connection-status');
        if (badge) {
            badge.textContent = message;
            badge.className = `status-badge ${type}`;
        }
    }
}

// Initialize
const monitor = new ConnectionMonitor();
```

### Latency & Connection Quality

```javascript
async function testConnectionSpeed() {
    const testUrl = '/api/dataset/disease';  // Test with a small endpoint
    const start = performance.now();
    
    try {
        const response = await fetch(testUrl);
        const end = performance.now();
        const latency = (end - start).toFixed(0);
        
        console.log(`📊 Latency: ${latency}ms`);
        
        if (latency < 200) console.log('✅ Excellent connection');
        else if (latency < 500) console.log('⚠️ Good connection');
        else if (latency < 1000) console.log('⚠️ Fair connection');
        else console.log('❌ Poor connection');
        
        return latency;
    } catch (error) {
        console.log('❌ Connection failed');
        return null;
    }
}

// Test periodically
setInterval(testConnectionSpeed, 30000);  // Every 30 seconds
```

---

## Prediction Cache Viewer

### View Recent Predictions

```javascript
async function viewRecentPredictions(limit = 10) {
    const predictions = await offlineManager.getFromIndexedDB('predictions');
    const recent = predictions.slice(-limit).reverse();
    
    console.table(recent.map(p => ({
        ID: p.id,
        Type: p.type,
        Time: new Date(p.timestamp).toLocaleString(),
        Synced: p.synced ? '✅' : '⏳',
        Result: p.result?.risk_level || p.result?.quantity_kg || 'N/A'
    })));
}

// Usage
viewRecentPredictions(5);
```

### Export Predictions to CSV

```javascript
async function exportPredictionsCSV() {
    const predictions = await offlineManager.getFromIndexedDB('predictions');
    
    // Create CSV header
    let csv = 'ID,Type,Timestamp,Input,Result,Synced\n';
    
    // Add rows
    predictions.forEach(p => {
        csv += `${p.id},"${p.type}","${p.timestamp}","${JSON.stringify(p.input)}","${JSON.stringify(p.result)}",${p.synced}\n`;
    });
    
    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `predictions-${new Date().toISOString()}.csv`;
    link.click();
}

// Usage
exportPredictionsCSV();
```

---

## Debugging Tools

### Clear All Offline Data

```javascript
async function clearOfflineData() {
    // Clear IndexedDB
    indexedDB.deleteDatabase('AquaSphereDB');
    
    // Clear Service Worker cache
    caches.keys().then(names => {
        names.forEach(name => caches.delete(name));
    });
    
    // Clear localStorage
    localStorage.clear();
    
    console.log('✅ All offline data cleared');
    window.location.reload();
}

// Usage (type in console):
// clearOfflineData();
```

### Reinitialize Offline Manager

```javascript
async function reinitOfflineManager() {
    // Wait for service worker
    await navigator.serviceWorker.ready;
    
    // Reinit manager
    window.offlineManager = new OfflineManager();
    
    console.log('✅ OfflineManager reinitialized');
}

// Usage
reinitOfflineManager();
```

### Full System Status Report

```javascript
async function getSystemStatus() {
    const storage = await navigator.storage.estimate();
    const sw = await navigator.serviceWorker.getRegistrations();
    const predictions = await offlineManager.getFromIndexedDB('predictions');
    const datasets = {};
    
    for (const name of ['disease', 'location', 'feed', 'yield', 'buyer', 'stocking', 'seed']) {
        const data = await offlineManager.getFromIndexedDB(name);
        datasets[name] = data?.length || 0;
    }
    
    return {
        online: navigator.onLine,
        serviceWorkers: sw.length,
        storage: {
            used: `${(storage.usage / 1024 / 1024).toFixed(2)} MB`,
            quota: `${(storage.quota / 1024 / 1024).toFixed(2)} MB`,
            percentage: `${(storage.usage / storage.quota * 100).toFixed(1)}%`
        },
        predictions: {
            total: predictions.length,
            synced: predictions.filter(p => p.synced).length,
            pending: predictions.filter(p => !p.synced).length
        },
        datasets,
        timestamp: new Date().toISOString()
    };
}

// Usage
getSystemStatus().then(status => console.table(status));
```

---

## Performance Monitoring

### Track Offline Prediction Speed

```javascript
async function benchmarkOfflinePredictions() {
    const tests = 100;
    const times = [];
    
    for (let i = 0; i < tests; i++) {
        const start = performance.now();
        await offlineManager.predictDisease(28, 7.5, 6, 15, 30);
        const end = performance.now();
        times.push(end - start);
    }
    
    const avg = times.reduce((a, b) => a + b) / times.length;
    const min = Math.min(...times);
    const max = Math.max(...times);
    
    console.log(`
        Offline Prediction Speed (${tests} tests):
        Average: ${avg.toFixed(2)}ms
        Min: ${min.toFixed(2)}ms
        Max: ${max.toFixed(2)}ms
    `);
}

// Usage
benchmarkOfflinePredictions();
```

---

## Alert & Notification System

### Offline Status Notifications

```javascript
function setupNotifications() {
    window.addEventListener('offline', () => {
        showNotification(
            '📡 You are offline',
            'The app will now use cached data for predictions',
            'info'
        );
    });

    window.addEventListener('online', () => {
        showNotification(
            '🌐 You are back online!',
            'Syncing offline predictions...',
            'success'
        );
    });
}

function showNotification(title, message, type = 'info') {
    // Browser notification
    if (Notification.permission === 'granted') {
        new Notification(title, {
            body: message,
            icon: '/static/img/icon.png'
        });
    }
    
    // Toast notification (UI)
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = `${title}: ${message}`;
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 3000);
}

// Request permission
if (Notification.permission === 'default') {
    Notification.requestPermission();
}
```

---

## Integration with Monitoring Services

### Send Metrics to Server

```javascript
async function reportOfflineMetrics() {
    const status = await getSystemStatus();
    
    try {
        await fetch('/api/metrics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                online: status.online,
                storageUsed: status.storage.used,
                predictions: status.predictions,
                timestamp: status.timestamp
            })
        });
    } catch (error) {
        console.log('Metrics reporting failed (expected offline):', error);
    }
}

// Report every 5 minutes
setInterval(reportOfflineMetrics, 5 * 60 * 1000);
```

---

## Dashboard Refresh Endpoint

Add this to Flask app for live dashboard updates:

```python
@app.route('/api/offline-stats')
def get_offline_stats():
    """Get current offline statistics for dashboard"""
    import os
    
    stats = {
        'timestamp': datetime.now().isoformat(),
        'datasets': {},
        'predictions': {
            'total': 0,
            'synced': 0,
            'pending': 0
        }
    }
    
    # Check datasets
    for dataset in ['disease', 'location', 'feed', 'yield', 'buyer', 'stocking', 'seed']:
        path = f'dataset/{dataset}.csv'
        if os.path.exists(path):
            size = os.path.getsize(path)
            stats['datasets'][dataset] = {
                'available': True,
                'size_mb': round(size / 1024 / 1024, 2)
            }
    
    # Load predictions
    try:
        preds = load_json('offline_predictions.json', [])
        stats['predictions']['total'] = len(preds)
        stats['predictions']['synced'] = len([p for p in preds if p.get('synced', False)])
        stats['predictions']['pending'] = stats['predictions']['total'] - stats['predictions']['synced']
    except:
        pass
    
    return jsonify(stats)
```

---

**Last Updated**: January 2026 | **Version**: 1.0
