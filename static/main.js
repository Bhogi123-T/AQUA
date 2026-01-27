// AquaSphereAI 2.0 Live Simulation Logic + Offline Support

// Global flag to control all live data fetching
window.ALLOW_LIVE_DATA = navigator.onLine;

/**
 * Real-time Connection Status Monitor
 */
function initializeConnectionMonitor() {
    const updateConnectionStatus = () => {
        const badge = document.getElementById('connection-badge');
        const icon = document.getElementById('connection-icon');
        const text = document.getElementById('connection-text');
        
        if (!badge) return;
        
        if (navigator.onLine) {
            // Online - show green badge with globe icon
            badge.style.background = 'rgba(0, 255, 136, 0.2)';
            badge.style.borderColor = 'rgba(0, 255, 136, 0.5)';
            badge.style.color = '#00ff88';
            icon.textContent = '🌐';
            text.textContent = 'ONLINE';
            
            // Enable live data
            window.ALLOW_LIVE_DATA = true;
            
            // Show live data sections and update all badges
            showLiveDataSections();
            updateLiveOfflineLabels(true);
        } else {
            // Offline - show red badge with warning icon
            badge.style.background = 'rgba(255, 0, 85, 0.2)';
            badge.style.borderColor = 'rgba(255, 0, 85, 0.5)';
            badge.style.color = '#ff0055';
            icon.textContent = '📡';
            text.textContent = 'OFFLINE';
            
            // Disable live data - STOP ALL EXTERNAL CALLS
            window.ALLOW_LIVE_DATA = false;
            
            // Hide live data sections and update all badges
            hideLiveDataSections();
            updateLiveOfflineLabels(false);
        }
    };
    
    // Update on page load
    updateConnectionStatus();
    
    // Update on connection change
    window.addEventListener('online', () => {
        window.ALLOW_LIVE_DATA = true;
        updateConnectionStatus();
        console.log('✅ Connection restored - ONLINE');
        showNotification('🌐 You are back online!', 'success');
    });
    
    window.addEventListener('offline', () => {
        window.ALLOW_LIVE_DATA = false;
        updateConnectionStatus();
        console.log('📡 Connection lost - OFFLINE MODE - ALL LIVE DATA DISABLED');
        showNotification('📡 You are now offline - Cached data only', 'info');
    });
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
 */
function updateLiveOfflineLabels(isOnline) {
    // Update badge text
    const badgeText = document.getElementById('connection-text');
    if (badgeText) {
        badgeText.textContent = isOnline ? 'ONLINE' : 'OFFLINE';
    }
    
    // Strategy: Find and replace specific badge elements
    const liveBadges = document.querySelectorAll('.live-pulse-badge');
    
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
