// AquaSphereAI 2.0 Live Simulation Logic + Offline Support

// Global flags
window.ALLOW_LIVE_DATA = navigator.onLine;
window.LOCATION_ENABLED = false;
window.LOCATION_CHECK_DONE = false;

/**
 * Check Location Permission - Required for Live Data
 */
async function checkLocationPermission() {
    if (window.LOCATION_CHECK_DONE) return window.LOCATION_ENABLED;

    window.LOCATION_CHECK_DONE = true;

    try {
        // Check if geolocation is available
        if (!('geolocation' in navigator)) {
            console.warn('⚠️ Geolocation not supported by browser');
            showLocationNotification('Your browser does not support location services');
            window.LOCATION_ENABLED = false;
            return false;
        }

        // Try to get current position with timeout
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                resolve,
                reject,
                { timeout: 5000, enableHighAccuracy: false }
            );
        });

        // Location granted
        console.log('✅ Location permission granted');
        window.LOCATION_ENABLED = true;
        return true;

    } catch (error) {
        // Location denied or error
        console.warn('📍 Location permission denied or unavailable:', error.message);
        window.LOCATION_ENABLED = false;

        // Show notification to enable location
        showLocationNotification();

        // Disable live features
        disableLiveFeaturesNoLocation();

        return false;
    }
}

/**
 * Show notification to enable location
 */
function showLocationNotification(customMessage = null) {
    const message = customMessage || '📍 Please enable location services to access live data and real-time features.';

    // Create notification popup
    const notification = document.createElement('div');
    notification.id = 'location-notification';
    notification.style.cssText = `
        position: fixed;
        top: 80px;
        left: 50%;
        transform: translateX(-50%);
        background: linear-gradient(135deg, #ff6b35, #ff0055);
        color: white;
        padding: 1.5rem 2rem;
        border-radius: 16px;
        box-shadow: 0 10px 40px rgba(255, 0, 85, 0.4);
        z-index: 9999;
        max-width: 90%;
        width: 400px;
        text-align: center;
        animation: slideDown 0.5s ease-out;
        font-family: 'Inter', sans-serif;
    `;

    notification.innerHTML = `
        <div style="font-size: 2rem; margin-bottom: 0.5rem;">📍</div>
        <div style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.5rem;">
            Location Required
        </div>
        <div style="font-size: 0.9rem; line-height: 1.5; margin-bottom: 1rem; opacity: 0.9;">
            ${message}
        </div>
        <button onclick="requestLocationPermission()" style="
            background: white;
            color: #ff0055;
            border: none;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            margin-right: 0.5rem;
            font-size: 0.9rem;
        ">
            Enable Location
        </button>
        <button onclick="closeLocationNotification()" style="
            background: rgba(255,255,255,0.2);
            color: white;
            border: 2px solid white;
            padding: 0.75rem 1.5rem;
            border-radius: 12px;
            font-weight: 700;
            cursor: pointer;
            font-size: 0.9rem;
        ">
            Maybe Later
        </button>
    `;

    // Add animation
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideDown {
            from {
                transform: translateX(-50%) translateY(-100px);
                opacity: 0;
            }
            to {
                transform: translateX(-50%) translateY(0);
                opacity: 1;
            }
        }
    `;
    document.head.appendChild(style);

    // Remove existing notification if any
    const existing = document.getElementById('location-notification');
    if (existing) existing.remove();

    document.body.appendChild(notification);

    // Auto-hide after 10 seconds
    setTimeout(() => {
        closeLocationNotification();
    }, 10000);
}

/**
 * Request location permission from user
 */
async function requestLocationPermission() {
    closeLocationNotification();

    try {
        const position = await new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                resolve,
                reject,
                { enableHighAccuracy: true }
            );
        });

        window.LOCATION_ENABLED = true;
        window.ALLOW_LIVE_DATA = navigator.onLine;

        showNotification('✅ Location enabled! Live features activated.', 'success');

        // Re-enable live features
        if (navigator.onLine) {
            showLiveDataSections();
            updateLiveOfflineLabels(true);
        }

        // Reload connection monitor
        initializeConnectionMonitor();

    } catch (error) {
        showNotification('❌ Location permission denied. Live features disabled.', 'error');
        disableLiveFeaturesNoLocation();
    }
}

/**
 * Close location notification
 */
function closeLocationNotification() {
    const notification = document.getElementById('location-notification');
    if (notification) {
        notification.style.animation = 'slideDown 0.3s ease-in reverse';
        setTimeout(() => notification.remove(), 300);
    }
}

/**
 * Disable live features when location is not available
 * NOTE: This does NOT affect the app's online/offline status badge!
 * The app can be ONLINE (connected to internet) but live data disabled (no location)
 */
function disableLiveFeaturesNoLocation() {
    console.log('📍 Location disabled - Hiding live data features (app still online)');

    // Disable live data flag - but DON'T change the connection badge
    window.ALLOW_LIVE_DATA = false;

    // Hide all live data sections
    hideLiveDataSections();

    // Show location-specific message in live data areas only
    showLocationRequiredMessage();
}

/**
 * Show location required message in live data areas
 */
function showLocationRequiredMessage() {
    const liveElements = document.querySelectorAll('[data-live-only]');
    liveElements.forEach(el => {
        // Add location required indicator (different from offline)
        if (!el.querySelector('[data-location-indicator]')) {
            const indicator = document.createElement('div');
            indicator.setAttribute('data-location-indicator', 'true');
            indicator.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255, 107, 53, 0.3);
                border: 1px solid #ff6b35;
                color: #ff6b35;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: bold;
                pointer-events: auto;
            `;
            indicator.textContent = '📍 LOCATION REQUIRED';
            el.style.position = 'relative';
            el.appendChild(indicator);
        }
    });
}

/**
 * Real-time Connection Status Monitor
 * Separates: 1) Internet connectivity (badge) from 2) Live data availability (location)
 */
function initializeConnectionMonitor() {
    const updateConnectionStatus = async () => {
        const badge = document.getElementById('connection-badge');
        const icon = document.getElementById('connection-icon');
        const text = document.getElementById('connection-text');

        if (!badge) return;

        // STEP 1: Update connection badge based ONLY on internet connectivity
        if (navigator.onLine) {
            // Online - show green badge with globe icon
            badge.style.background = 'rgba(0, 255, 136, 0.2)';
            badge.style.borderColor = 'rgba(0, 255, 136, 0.5)';
            badge.style.color = '#00ff88';
            badge.classList.remove('offline');
            if (icon) icon.textContent = '🌐';
            if (text) text.textContent = 'ONLINE';
        } else {
            // Offline - show red badge with warning icon
            badge.style.background = 'rgba(255, 0, 85, 0.2)';
            badge.style.borderColor = 'rgba(255, 0, 85, 0.5)';
            badge.style.color = '#ff0055';
            badge.classList.add('offline');
            if (icon) icon.textContent = '📡';
            if (text) text.textContent = 'OFFLINE';
        }

        // STEP 2: Check location permission for live data features (separate from badge)
        const hasLocation = await checkLocationPermission();

        // STEP 3: Determine if live data should be available
        // Live data requires BOTH internet AND location
        if (navigator.onLine && hasLocation) {
            // Both internet AND location - enable live data
            window.ALLOW_LIVE_DATA = true;
            showLiveDataSections();
            updateLiveOfflineLabels(true);
        } else if (navigator.onLine && !hasLocation) {
            // Internet ON, Location OFF - app is online, but live data disabled
            window.ALLOW_LIVE_DATA = false;
            hideLiveDataSections();
            showLocationRequiredMessage();
            // Keep the LIVE badges as offline, but connection badge stays ONLINE
            updateLiveDataBadges(false);
        } else {
            // No internet - everything offline
            window.ALLOW_LIVE_DATA = false;
            hideLiveDataSections();
            updateLiveOfflineLabels(false);
        }
    };

    // Update on page load
    updateConnectionStatus();

    // Update on connection change
    window.addEventListener('online', () => {
        console.log('✅ Connection restored - ONLINE');
        showNotification('🌐 You are back online!', 'success');
        updateConnectionStatus();
    });

    window.addEventListener('offline', () => {
        window.ALLOW_LIVE_DATA = false;
        console.log('📡 Connection lost - OFFLINE MODE - ALL LIVE DATA DISABLED');
        showNotification('📡 You are now offline - Cached data only', 'info');
        updateConnectionStatus();
    });
}

/**
 * Update only the live data badges (not the connection badge)
 */
function updateLiveDataBadges(isLive) {
    // Update live pulse badges (but NOT the connection badge)
    const liveBadges = document.querySelectorAll('.live-pulse-badge:not(#connection-badge)');

    liveBadges.forEach(badge => {
        const badgeType = badge.getAttribute('data-badge-type');

        if (isLive) {
            // Show as LIVE
            if (badgeType === 'realtime') {
                badge.textContent = '🔴 LIVE';
                badge.style.color = '#00ff88';
                badge.style.background = 'rgba(0, 255, 136, 0.2)';
                badge.style.borderColor = 'rgba(0, 255, 136, 0.5)';
            } else if (badgeType === 'sensors') {
                badge.textContent = '🔴 SENSORS ACTIVE';
                badge.style.color = '#00d2ff';
                badge.style.background = 'rgba(0, 210, 255, 0.2)';
                badge.style.borderColor = 'rgba(0, 210, 255, 0.5)';
            } else if (badgeType === 'market') {
                badge.textContent = '🔴 LIVE TELEMETRY';
                badge.style.color = '#00d2ff';
                badge.style.background = 'rgba(0, 210, 255, 0.2)';
                badge.style.borderColor = 'rgba(0, 210, 255, 0.5)';
            }
        } else {
            // Show as LOCATION REQUIRED (orange, not red)
            badge.textContent = '📍 LOCATION OFF';
            badge.style.color = '#ff6b35';
            badge.style.background = 'rgba(255, 107, 53, 0.2)';
            badge.style.borderColor = 'rgba(255, 107, 53, 0.5)';
        }
    });

    // Update ticker text for live data status
    const tickerLiveText = document.getElementById('ticker-live-text');
    if (tickerLiveText) {
        if (isLive) {
            tickerLiveText.textContent = 'LIVE';
            tickerLiveText.style.color = '#00ff88';
        } else {
            tickerLiveText.textContent = 'LOCATION OFF';
            tickerLiveText.style.color = '#ff6b35';
        }
    }
}

/**
 * Show live data sections when online - ALSO UPDATE ALL LIVE/OFFLINE LABELS
 */
function showLiveDataSections() {
    const liveElements = document.querySelectorAll('[data-live-only]');
    liveElements.forEach(el => {
        // Keep visible and show as ACTIVE
        el.style.display = 'block';
        el.style.opacity = '1';
        el.style.pointerEvents = 'auto';
        el.classList.remove('offline-state');
        el.classList.add('online-state');

        // Remove grayscale filter
        el.style.filter = 'none';

        // Re-enable all buttons in this section
        const buttons = el.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.disabled = false;
            btn.style.opacity = '1';
            btn.style.cursor = 'pointer';
        });

        // Remove offline indicators
        const indicators = el.querySelectorAll('[data-offline-indicator]');
        indicators.forEach(ind => ind.remove());
    });

    // Change all "OFFLINE" labels back to "LIVE" when online
    updateLiveOfflineLabels(true);

    // Update ticker with live data
    updateLiveData();
}

/**
 * Hide live data sections and show cached data when offline - CHANGE ALL LABELS TO OFFLINE
 */
function hideLiveDataSections() {
    const liveElements = document.querySelectorAll('[data-live-only]');
    liveElements.forEach(el => {
        // KEEP VISIBLE but show as OFFLINE/DISABLED
        el.style.display = 'block';
        el.style.opacity = '0.75';
        el.style.pointerEvents = 'none';
        el.classList.add('offline-state');
        el.classList.remove('online-state');

        // Add grayscale effect to show offline
        el.style.filter = 'grayscale(60%) brightness(0.9)';

        // Disable all buttons in this section
        const buttons = el.querySelectorAll('button');
        buttons.forEach(btn => {
            btn.disabled = true;
            btn.style.opacity = '0.6';
            btn.style.cursor = 'not-allowed';
        });

        // Add offline indicator to cards
        if (!el.querySelector('[data-offline-indicator]')) {
            const indicator = document.createElement('div');
            indicator.setAttribute('data-offline-indicator', 'true');
            indicator.style.cssText = `
                position: absolute;
                top: 10px;
                right: 10px;
                background: rgba(255, 0, 85, 0.3);
                border: 1px solid #ff0055;
                color: #ff0055;
                padding: 4px 8px;
                border-radius: 4px;
                font-size: 0.7rem;
                font-weight: bold;
                pointer-events: auto;
            `;
            indicator.textContent = '📡 OFFLINE';
            el.style.position = 'relative';
            el.appendChild(indicator);
        }
    });

    // Change all "LIVE" labels to "OFFLINE" when offline
    updateLiveOfflineLabels(false);

    // Show offline message in ticker
    const ticker = document.querySelector('.ticker-content');
    if (ticker) {
        const offlineMsg = ticker.querySelector('[data-offline-msg]');
        if (!offlineMsg) {
            const msg = document.createElement('span');
            msg.className = 'ticker-item';
            msg.setAttribute('data-offline-msg', 'true');
            msg.innerHTML = '📡 <strong>OFFLINE MODE:</strong> Using cached farm data';
            msg.style.color = '#ff0055';
            msg.style.fontWeight = 'bold';
            ticker.insertBefore(msg, ticker.firstChild.nextSibling);
        }
    }
}

/**
 * Replace all LIVE indicators with OFFLINE and vice versa
 * NOTE: This function should NOT modify the main connection badge (#connection-badge)
 * The connection badge is ONLY controlled by internet connectivity status
 */
function updateLiveOfflineLabels(isOnline) {
    // DO NOT update the main connection badge here!
    // The connection badge is managed separately based on internet connectivity only

    // Strategy: Find and replace specific badge elements
    // IMPORTANT: Exclude the #connection-badge - it should only reflect internet status
    const liveBadges = document.querySelectorAll('.live-pulse-badge:not(#connection-badge)');

    liveBadges.forEach(badge => {
        const badgeType = badge.getAttribute('data-badge-type');

        if (isOnline) {
            // Show LIVE badges
            if (badgeType === 'realtime') {
                badge.textContent = '🔴 LIVE';
                badge.style.color = '#00ff88';
                badge.style.background = 'rgba(0, 255, 136, 0.2)';
                badge.style.borderColor = 'rgba(0, 255, 136, 0.5)';
            } else if (badgeType === 'sensors') {
                badge.textContent = '🔴 SENSORS ACTIVE';
                badge.style.color = '#00d2ff';
                badge.style.background = 'rgba(0, 210, 255, 0.2)';
                badge.style.borderColor = 'rgba(0, 210, 255, 0.5)';
            } else if (badgeType === 'market') {
                badge.textContent = '🔴 LIVE TELEMETRY';
                badge.style.color = '#00d2ff';
                badge.style.background = 'rgba(0, 210, 255, 0.2)';
                badge.style.borderColor = 'rgba(0, 210, 255, 0.5)';
            }
        } else {
            // Show OFFLINE badges
            if (badgeType === 'realtime') {
                badge.textContent = '📡 OFFLINE';
                badge.style.color = '#ff0055';
                badge.style.background = 'rgba(255, 0, 85, 0.2)';
                badge.style.borderColor = 'rgba(255, 0, 85, 0.5)';
            } else if (badgeType === 'sensors') {
                badge.textContent = '📡 OFFLINE';
                badge.style.color = '#ff0055';
                badge.style.background = 'rgba(255, 0, 85, 0.2)';
                badge.style.borderColor = 'rgba(255, 0, 85, 0.5)';
            } else if (badgeType === 'market') {
                badge.textContent = '📡 OFFLINE TELEMETRY';
                badge.style.color = '#ff0055';
                badge.style.background = 'rgba(255, 0, 85, 0.2)';
                badge.style.borderColor = 'rgba(255, 0, 85, 0.5)';
            }
        }
    });

    // Update status badge text elements
    const statusBadges = document.querySelectorAll('.status-badge-text');
    statusBadges.forEach(badge => {
        badge.textContent = isOnline ? 'LIVE' : 'OFFLINE';
        badge.style.color = isOnline ? '#00ff88' : '#ff0055';
    });

    // Update live pulse animation
    const livePulses = document.querySelectorAll('.live-pulse');
    livePulses.forEach(pulse => {
        if (isOnline) {
            pulse.style.animation = 'pulse 2s infinite';
            pulse.style.background = '#00ff88';
            pulse.style.opacity = '1';
        } else {
            pulse.style.animation = 'none';
            pulse.style.background = '#ff0055';
            pulse.style.opacity = '0.3';
        }
    });

    // Update header sections
    const headers = document.querySelectorAll('h2, h3');
    headers.forEach(h => {
        const text = h.innerText;
        if (isOnline && text.includes('🛰️')) {
            // Keep LIVE for headers
            h.style.opacity = '1';
        } else if (!isOnline && text.includes('🛰️')) {
            // Dim or adjust offline headers
            h.style.opacity = '0.7';
        }
    });

    // Update ticker live/offline text
    const tickerLiveText = document.getElementById('ticker-live-text');
    if (tickerLiveText) {
        tickerLiveText.textContent = isOnline ? 'LIVE' : 'OFFLINE';
        tickerLiveText.style.color = isOnline ? '#00ff88' : '#ff0055';
    }
}

/**
 * Update live data when online
 */
function updateLiveData() {
    // Remove offline message if exists
    const offlineMsg = document.querySelector('[data-offline-msg]');
    if (offlineMsg) {
        offlineMsg.remove();
    }
}

/**
 * Show notification to user
 */
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? 'rgba(0, 255, 136, 0.2)' : 'rgba(0, 210, 255, 0.2)'};
        border: 1px solid ${type === 'success' ? 'rgba(0, 255, 136, 0.5)' : 'rgba(0, 210, 255, 0.5)'};
        color: ${type === 'success' ? '#00ff88' : '#00d2ff'};
        border-radius: 12px;
        z-index: 5000;
        animation: slideIn 0.3s ease;
        font-weight: 600;
        max-width: 300px;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 4000);
}

// Add slide animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(400px);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

document.addEventListener('DOMContentLoaded', () => {
    // Initialize connection monitor
    initializeConnectionMonitor();

    const tickerContainer = document.querySelector('.ticker-content');

    // Simulate real-time environmental fluctuations (only when online and LIVE DATA enabled)
    setInterval(() => {
        if (!navigator.onLine || !window.ALLOW_LIVE_DATA) return;
        const tempItem = Array.from(document.querySelectorAll('.ticker-item')).find(el => el.innerText.includes('🌡️'));
        if (tempItem) {
            const currentTemp = 28.6 + (Math.random() * 0.4 - 0.2);
            tempItem.innerHTML = `🌡️ Water: ${currentTemp.toFixed(1)}°C`;
        }

        const priceItem = Array.from(document.querySelectorAll('.ticker-item')).find(el => el.innerText.includes('🦐'));
        if (priceItem) {
            const currentPrice = 6.3 + (Math.random() * 0.1 - 0.05);
            priceItem.innerHTML = `🦐 Vannamei: $${currentPrice.toFixed(2)}/kg`;
        }
    }, 5000);

    // Form Auto-Fill Simulation (Live Tracking)
    const latField = document.querySelector('input[name="lat"]');
    const lonField = document.querySelector('input[name="lon"]');

    if (navigator.geolocation && (latField || lonField)) {
        navigator.geolocation.getCurrentPosition(position => {
            if (latField) latField.value = position.coords.latitude.toFixed(4);
            if (lonField) lonField.value = position.coords.longitude.toFixed(4);
        });
    }

    // PWA Install Logic
    let deferredPrompt;
    window.addEventListener('beforeinstallprompt', (e) => {
        e.preventDefault();
        deferredPrompt = e;
        console.log('PWA Install Prompt Ready');
    });

    window.installApp = async () => {
        if (deferredPrompt) {
            deferredPrompt.prompt();
            const { outcome } = await deferredPrompt.userChoice;
            console.log(`User response to the install prompt: ${outcome}`);
            deferredPrompt = null;
        } else {
            alert("To install: Tap the browser menu (or share button on iOS) and select 'Add to Home Screen'");
        }
    };

    // Register Service Worker for offline support
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/sw.js')
            .then(reg => console.log('✅ Service Worker registered for offline support'))
            .catch(err => console.log('Service Worker registration failed:', err));
    }

    // Intercept form submissions for offline handling
    setupOfflineFormHandling();
});

/**
 * Intercept prediction form submissions to use offline data when needed
 */
function setupOfflineFormHandling() {
    document.addEventListener('submit', async (e) => {
        const form = e.target;

        // Only intercept prediction forms
        if (!form.action.includes('/predict_') && !form.action.includes('/check_export')) {
            return;
        }

        e.preventDefault();

        // Check if online
        if (!navigator.onLine && window.offlineManager) {
            await handleOfflinePrediction(form);
        } else {
            // Submit normally (online)
            form.submit();
        }
    });
}

/**
 * Handle prediction when offline
 */
async function handleOfflinePrediction(form) {
    const formData = new FormData(form);
    const action = form.action;
    let prediction;

    try {
        if (action.includes('/predict_disease')) {
            prediction = await offlineManager.predictDisease(
                parseFloat(formData.get('temp')),
                parseFloat(formData.get('ph')),
                parseFloat(formData.get('do')),
                parseFloat(formData.get('salinity')),
                parseFloat(formData.get('turbidity'))
            );
            displayOfflinePrediction('Disease Prediction', prediction);
        } else if (action.includes('/predict_feed')) {
            prediction = await offlineManager.predictFeed(
                parseFloat(formData.get('age')),
                parseFloat(formData.get('avg_temp')),
                formData.get('species'),
                formData.get('feed_type')
            );
            displayOfflinePrediction('Feed Calculation', prediction);
        } else if (action.includes('/predict_yield')) {
            prediction = await offlineManager.predictYield(
                parseFloat(formData.get('total_feed')),
                parseFloat(formData.get('culture_dur')),
                formData.get('species'),
                formData.get('water_quality')
            );
            displayOfflinePrediction('Yield Forecast', prediction);
        } else if (action.includes('/market')) {
            prediction = await offlineManager.getMarketPrices();
            displayOfflineMarket(prediction);
        }

        // Save to IndexedDB for sync later
        if (prediction) {
            await offlineManager.savePrediction(
                action.split('/').pop(),
                Object.fromEntries(formData),
                prediction
            );
        }
    } catch (error) {
        console.error('Offline prediction error:', error);
        offlineManager.showNotification('❌ Could not generate offline prediction', 'error');
    }
}

/**
 * Display offline prediction result
 */
function displayOfflinePrediction(title, prediction) {
    const resultHTML = `
        <div class="offline-result">
            <h2>${title}</h2>
            <div class="offline-badge">📡 OFFLINE MODE (Demo Data)</div>
            <div class="result-content">
                ${Object.entries(prediction).map(([key, value]) => `
                    <div class="result-item">
                        <strong>${key.replace(/_/g, ' ')}:</strong> ${value}
                    </div>
                `).join('')}
            </div>
            <p class="sync-note">✓ This will sync to server when back online</p>
        </div>
    `;

    // Create modal or replace content
    const modal = document.createElement('div');
    modal.className = 'result-modal';
    modal.innerHTML = resultHTML;
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 30px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 9999;
        max-width: 500px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    `;

    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 9998;
    `;
    backdrop.onclick = () => {
        modal.remove();
        backdrop.remove();
    };

    document.body.appendChild(backdrop);
    document.body.appendChild(modal);
}

/**
 * Display offline market data
 */
function displayOfflineMarket(marketData) {
    const marketHTML = `
        <div class="offline-market">
            <h2>Market Prices (Offline Data)</h2>
            <div class="offline-badge">📡 OFFLINE MODE</div>
            <div class="market-table">
                ${marketData.map(item => `
                    <div class="market-item">
                        <span class="country">${item.country}</span>
                        <span class="species">${item.species}</span>
                        <span class="price">$${item.price}/kg</span>
                        <span class="qty">${item.qty} tons</span>
                    </div>
                `).join('')}
            </div>
        </div>
    `;

    const modal = document.createElement('div');
    modal.innerHTML = marketHTML;
    modal.style.cssText = `
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.2);
        z-index: 9999;
        max-width: 600px;
        width: 90%;
        max-height: 80vh;
        overflow-y: auto;
    `;

    const backdrop = document.createElement('div');
    backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0,0,0,0.5);
        z-index: 9998;
    `;
    backdrop.onclick = () => {
        modal.remove();
        backdrop.remove();
    };

    document.body.appendChild(backdrop);
    document.body.appendChild(modal);
}

/**
 * Show offline status indicator
 */
function showOfflineStatus() {
    const status = document.createElement('div');
    status.id = 'offline-indicator';
    status.style.cssText = `
        position: fixed;
        bottom: 20px;
        left: 20px;
        padding: 12px 16px;
        background: #ff9800;
        color: white;
        border-radius: 20px;
        font-size: 14px;
        z-index: 1000;
        display: none;
    `;
    status.textContent = '📡 Offline Mode';
    document.body.appendChild(status);

    window.addEventListener('offline', () => {
        status.style.display = 'block';
    });

    window.addEventListener('online', () => {
        status.style.display = 'none';
    });
}
