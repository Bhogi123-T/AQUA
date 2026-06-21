/**
 * OfflineManager - Handles all offline functionality for AquaSphere
 * - Syncs datasets to IndexedDB on app load
 * - Detects online/offline status
 * - Provides offline prediction fallbacks
 * - Manages data sync when back online
 */

class OfflineManager {
    constructor() {
        this.dbName = 'AquaSphereDB';
        this.version = 1;
        this.db = null;
        this.isOnline = navigator.onLine;
        this.datasets = {};
        this.init();
    }

    /**
     * Initialize IndexedDB and event listeners
     */
    async init() {
        await this.openDB();
        this.setupEventListeners();
        await this.loadDatasets();
        console.log('OfflineManager initialized. Online:', this.isOnline);
    }

    /**
     * Open or create IndexedDB
     */
    openDB() {
        return new Promise((resolve, reject) => {
            const request = indexedDB.open(this.dbName, this.version);

            request.onerror = () => reject(request.error);
            request.onsuccess = () => {
                this.db = request.result;
                resolve(this.db);
            };

            request.onupgradeneeded = (e) => {
                const db = e.target.result;

                // Create object stores for each dataset
                if (!db.objectStoreNames.contains('disease')) {
                    db.createObjectStore('disease', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('location')) {
                    db.createObjectStore('location', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('feed')) {
                    db.createObjectStore('feed', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('yield')) {
                    db.createObjectStore('yield', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('buyer')) {
                    db.createObjectStore('buyer', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('stocking')) {
                    db.createObjectStore('stocking', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('seed')) {
                    db.createObjectStore('seed', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('predictions')) {
                    db.createObjectStore('predictions', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('market')) {
                    db.createObjectStore('market', { keyPath: 'id', autoIncrement: true });
                }
                if (!db.objectStoreNames.contains('meta')) {
                    db.createObjectStore('meta');
                }
            };
        });
    }

    /**
     * Setup online/offline event listeners
     */
    setupEventListeners() {
        window.addEventListener('online', () => {
            this.isOnline = true;
            this.updateConnectionBadge();
            this.showNotification('🌐 You are back online!', 'success');
            this.syncPendingData();
        });

        window.addEventListener('offline', () => {
            this.isOnline = false;
            this.updateConnectionBadge();
            this.showNotification('📡 Working in offline mode', 'info');
        });

        // Update badge on initial page load
        document.addEventListener('DOMContentLoaded', () => {
            this.updateConnectionBadge();
        });
    }

    /**
     * Update the connection status badge below the logo
     */
    updateConnectionBadge() {
        const badge = document.getElementById('connection-badge');
        const icon = document.getElementById('connection-icon');
        const text = document.getElementById('connection-text');

        if (!badge || !icon || !text) return;

        if (this.isOnline) {
            badge.classList.remove('offline');
            icon.textContent = '🌐';
            text.textContent = 'ONLINE';
        } else {
            badge.classList.add('offline');
            icon.textContent = '📡';
            text.textContent = 'OFFLINE';
        }
    }

    /**
     * Load all datasets from server and store in IndexedDB
     */
    async loadDatasets() {
        const datasets = [
            'disease', 'location', 'feed', 'yield', 'buyer', 'stocking', 'seed'
        ];

        for (const dataset of datasets) {
            try {
                const response = await fetch(`/api/dataset/${dataset}`);
                if (response.ok) {
                    const data = await response.json();
                    await this.saveToIndexedDB(dataset, data);
                    this.datasets[dataset] = data;
                }
            } catch (error) {
                console.log(`Failed to load ${dataset} dataset:`, error);
                // Try to load from IndexedDB if network fails
                const cached = await this.getFromIndexedDB(dataset);
                if (cached) {
                    this.datasets[dataset] = cached;
                }
            }
        }

        // Load market data
        try {
            const marketData = await this.generateMarketData();
            await this.saveToIndexedDB('market', marketData);
            this.datasets['market'] = marketData;
        } catch (error) {
            console.log('Failed to load market data:', error);
        }
    }

    /**
     * Generate market data (simulated)
     */
    async generateMarketData() {
        return [
            { id: 1, country: "Norway", species: "Salmon", price: 12.5, qty: 45 },
            { id: 2, country: "Vietnam", species: "Vannamei", price: 6.8, qty: 120 },
            { id: 3, country: "India", species: "Tiger Prawn", price: 8.2, qty: 85 },
            { id: 4, country: "USA", species: "Catfish", price: 4.5, qty: 200 },
            { id: 5, country: "Brazil", species: "Tilapia", price: 3.2, qty: 300 },
            { id: 6, country: "China", species: "Mud Crab", price: 22.0, qty: 50 },
        ];
    }

    /**
     * Save data to IndexedDB
     */
    saveToIndexedDB(storeName, data) {
        return new Promise((resolve, reject) => {
            if (!this.db) return reject('DB not initialized');

            const transaction = this.db.transaction([storeName], 'readwrite');
            const store = transaction.objectStore(storeName);

            // Clear existing data
            const clearRequest = store.clear();
            clearRequest.onsuccess = () => {
                // Add new data
                if (Array.isArray(data)) {
                    data.forEach(item => {
                        store.add(item);
                    });
                } else {
                    store.add(data);
                }
            };

            transaction.oncomplete = () => resolve();
            transaction.onerror = () => reject(transaction.error);
        });
    }

    /**
     * Get all data from IndexedDB store
     */
    getFromIndexedDB(storeName) {
        return new Promise((resolve, reject) => {
            if (!this.db) return reject('DB not initialized');

            const transaction = this.db.transaction([storeName], 'readonly');
            const store = transaction.objectStore(storeName);
            const request = store.getAll();

            request.onsuccess = () => resolve(request.result);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Make offline prediction for disease based on cached data
     */
    async predictDisease(waterTemp, pH, DO, salinity, turbidity) {
        const data = this.datasets['disease'] || await this.getFromIndexedDB('disease');

        if (!data || data.length === 0) {
            return this.getDemoDiseasePrediction();
        }

        // Find closest matching records in dataset
        const matches = data.filter(row => {
            return Math.abs(row.Water_Temp - waterTemp) < 3 &&
                Math.abs(row.pH - pH) < 0.5 &&
                Math.abs(row.DO - DO) < 1 &&
                Math.abs(row.Salinity - salinity) < 2 &&
                Math.abs(row.Turbidity - turbidity) < 10;
        });

        if (matches.length > 0) {
            const avgRisk = matches.reduce((sum, m) => sum + m.Disease_Risk, 0) / matches.length;
            return {
                risk_level: avgRisk > 0.5 ? 'HIGH' : 'LOW',
                disease_type: matches[0].Disease_Type || 'None',
                medicine: matches[0].Suggested_Medicine || 'Monitor water quality',
                confidence: (matches.length / data.length * 100).toFixed(0),
                offline: true
            };
        }

        return this.getDemoDiseasePrediction();
    }

    /**
     * Make offline prediction for feed calculation
     */
    async predictFeed(age, waterTemp, species, feedType) {
        const data = this.datasets['feed'] || await this.getFromIndexedDB('feed');

        if (!data || data.length === 0) {
            return this.getDemoFeedPrediction();
        }

        const matches = data.filter(row => {
            return Math.abs(row.Age_Days - age) < 10 &&
                Math.abs(row.Avg_Temp - waterTemp) < 2;
        });

        if (matches.length > 0) {
            const avgQuantity = matches.reduce((sum, m) => sum + parseFloat(m.Quantity_kg || 0), 0) / matches.length;
            return {
                quantity_kg: avgQuantity.toFixed(2),
                fcr: (matches[0].FCR || 1.5).toFixed(2),
                frequency: matches[0].Frequency || '2-3 times daily',
                offline: true
            };
        }

        return this.getDemoFeedPrediction();
    }

    /**
     * Get offline yield prediction
     */
    async predictYield(totalFeed, cultureDuration, species, waterQuality) {
        const data = this.datasets['yield'] || await this.getFromIndexedDB('yield');

        if (!data || data.length === 0) {
            return this.getDemoYieldPrediction();
        }

        const avgYield = data.reduce((sum, row) => sum + parseFloat(row.Yield_kg || 0), 0) / data.length;
        return {
            estimated_yield_kg: (avgYield * (totalFeed / 100)).toFixed(2),
            profitability: 'Moderate',
            recommendation: 'Maintain consistent feeding and water quality monitoring',
            offline: true
        };
    }

    /**
     * Get market prices from cached data
     */
    async getMarketPrices() {
        const data = this.datasets['market'] || await this.getFromIndexedDB('market');

        if (!data || data.length === 0) {
            return this.getDemoMarketData();
        }

        return data.map(item => ({
            ...item,
            price_inr: (item.price * 83).toFixed(2),
            last_update: new Date().toLocaleTimeString(),
            offline: true
        }));
    }

    /**
     * Save offline prediction to IndexedDB for sync later
     */
    async savePrediction(type, inputs, output) {
        const prediction = {
            type,
            inputs,
            output,
            timestamp: new Date().toISOString(),
            synced: false
        };

        return new Promise((resolve, reject) => {
            if (!this.db) return reject('DB not initialized');

            const transaction = this.db.transaction(['predictions'], 'readwrite');
            const store = transaction.objectStore('predictions');
            const request = store.add(prediction);

            request.onsuccess = () => resolve(prediction);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Sync pending predictions when back online
     */
    async syncPendingData() {
        if (!this.isOnline) return;

        try {
            const predictions = await this.getFromIndexedDB('predictions');
            const unsynced = predictions.filter(p => !p.synced);

            for (const pred of unsynced) {
                // Send to server endpoint
                const response = await fetch('/api/sync-prediction', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(pred)
                });

                if (response.ok) {
                    // Mark as synced
                    pred.synced = true;
                    await this.updatePrediction(pred);
                }
            }

            console.log(`Synced ${unsynced.length} predictions`);
        } catch (error) {
            console.log('Sync failed:', error);
        }
    }

    /**
     * Update prediction record
     */
    updatePrediction(prediction) {
        return new Promise((resolve, reject) => {
            if (!this.db) return reject('DB not initialized');

            const transaction = this.db.transaction(['predictions'], 'readwrite');
            const store = transaction.objectStore('predictions');
            const request = store.put(prediction);

            request.onsuccess = () => resolve(prediction);
            request.onerror = () => reject(request.error);
        });
    }

    /**
     * Demo predictions for when data is unavailable
     */
    getDemoDiseasePrediction() {
        return {
            risk_level: 'MODERATE',
            disease_type: 'White Spot',
            medicine: 'Lime Treatment (Calcium Hydroxide)',
            confidence: 45,
            offline: true,
            demo: true
        };
    }

    getDemoFeedPrediction() {
        return {
            quantity_kg: 15.5,
            fcr: 1.8,
            frequency: '2 times daily',
            offline: true,
            demo: true
        };
    }

    getDemoYieldPrediction() {
        return {
            estimated_yield_kg: 850,
            profitability: 'Moderate',
            recommendation: 'Monitor water parameters closely',
            offline: true,
            demo: true
        };
    }

    getDemoMarketData() {
        return [
            { id: 1, country: "India", species: "Vannamei", price: 6.5, price_inr: 539.5, qty: 100, offline: true },
            { id: 2, country: "Vietnam", species: "Shrimp", price: 7.0, price_inr: 581, qty: 150, offline: true },
            { id: 3, country: "Norway", species: "Salmon", price: 12, price_inr: 996, qty: 50, offline: true },
        ];
    }

    /**
     * Show offline/online notifications
     */
    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `offline-notification ${type}`;
        notification.innerHTML = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            background: ${type === 'success' ? '#4CAF50' : type === 'error' ? '#f44336' : '#2196F3'};
            color: white;
            z-index: 10000;
            font-weight: bold;
            animation: slideIn 0.3s ease-out;
        `;
        document.body.appendChild(notification);

        setTimeout(() => notification.remove(), 4000);
    }

    /**
     * Get offline status
     */
    getStatus() {
        return {
            online: this.isOnline,
            cachedDatasets: Object.keys(this.datasets).length,
            lastSync: localStorage.getItem('lastSync') || 'Never'
        };
    }
}

// Initialize on page load
const offlineManager = new OfflineManager();
