const CACHE_VERSION = 'aqua-offline-v4';
const STATIC_CACHE = `${CACHE_VERSION}-static`;
const PAGES_CACHE = `${CACHE_VERSION}-pages`;
const RUNTIME_CACHE = `${CACHE_VERSION}-runtime`;

// Core static assets - MUST be cached for offline
const STATIC_ASSETS = [
    '/static/style.css',
    '/static/main.js',
    '/static/offline-manager.js',
    '/static/manifest.json',
    '/static/logo.png',
    '/static/splash.png'
];

// External resources - Try to cache but don't fail if unavailable
const EXTERNAL_ASSETS = [
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap',
    'https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js',
    'https://unpkg.com/html5-qrcode@2.3.8/html5-qrcode.min.js'
];

// ALL app pages - Pre-cache during install for complete offline access
const APP_PAGES = [
    '/',
    '/farmer',
    '/buyer',
    '/market',
    '/location',
    '/logistics',
    '/districts',
    '/technicians',
    '/knowledge',
    '/settings',
    '/qr-scanner',
    '/precautions',
    '/login',
    '/signup'
];

// Install - Aggressively cache everything needed for offline
self.addEventListener('install', (event) => {
    console.log('[SW] Installing... Pre-caching all resources for offline');

    event.waitUntil(
        Promise.all([
            // Cache static assets (critical)
            caches.open(STATIC_CACHE).then(cache => {
                console.log('[SW] Caching static assets');
                return cache.addAll(STATIC_ASSETS)
                    .then(() => console.log('[SW] ✓ Static assets cached'))
                    .catch(err => {
                        console.error('[SW] ✗ Failed to cache static assets:', err);
                        throw err; // Critical failure
                    });
            }),

            // Cache all HTML pages (critical for offline)
            caches.open(PAGES_CACHE).then(cache => {
                console.log('[SW] Caching all app pages');
                return Promise.allSettled(
                    APP_PAGES.map(url => {
                        return fetch(url)
                            .then(response => {
                                if (response.ok) {
                                    return cache.put(url, response);
                                }
                                throw new Error(`Failed to fetch ${url}`);
                            })
                            .catch(err => {
                                console.warn(`[SW] Could not cache page: ${url}`, err);
                            });
                    })
                ).then(results => {
                    const successful = results.filter(r => r.status === 'fulfilled').length;
                    console.log(`[SW] ✓ Cached ${successful}/${APP_PAGES.length} pages`);
                });
            }),

            // Cache external assets (non-critical)
            caches.open(STATIC_CACHE).then(cache => {
                console.log('[SW] Caching external assets');
                return Promise.allSettled(
                    EXTERNAL_ASSETS.map(url => {
                        return fetch(url, { mode: 'cors' })
                            .then(response => {
                                if (response.ok) {
                                    return cache.put(url, response);
                                }
                            })
                            .catch(err => {
                                console.warn(`[SW] Could not cache external: ${url}`, err);
                            });
                    })
                ).then(() => console.log('[SW] ✓ External assets cached'));
            })
        ])
            .then(() => {
                console.log('[SW] ✅ Installation complete - App ready for offline use');
                return self.skipWaiting();
            })
            .catch(err => {
                console.error('[SW] ❌ Installation failed:', err);
                throw err;
            })
    );
});

// Activate - Clean old caches and take control
self.addEventListener('activate', (event) => {
    console.log('[SW] Activating...');

    event.waitUntil(
        caches.keys()
            .then(cacheNames => {
                return Promise.all(
                    cacheNames
                        .filter(name => !name.startsWith(CACHE_VERSION))
                        .map(name => {
                            console.log('[SW] Deleting old cache:', name);
                            return caches.delete(name);
                        })
                );
            })
            .then(() => {
                console.log('[SW] ✅ Activated - Taking control of all clients');
                return self.clients.claim();
            })
    );
});

// Fetch - Smart offline-first strategy
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);

    // Only handle GET requests
    if (request.method !== 'GET') {
        return;
    }

    // Skip non-same-origin requests except for allowed domains
    if (url.origin !== self.location.origin) {
        if (isAllowedExternal(url.hostname)) {
            event.respondWith(cacheFirstExternal(request));
        }
        return;
    }

    // Route requests to appropriate strategy
    if (isStaticAsset(url.pathname)) {
        // Static files: Cache First (fastest)
        event.respondWith(cacheFirst(request));
    } else if (isHTMLPage(request)) {
        // HTML pages: Cache First with Network Update (works offline)
        event.respondWith(cacheFirstWithUpdate(request));
    } else {
        // Everything else: Network First with Cache Fallback
        event.respondWith(networkFirst(request));
    }
});

// Helper: Check if URL is static asset
function isStaticAsset(pathname) {
    return pathname.startsWith('/static/') ||
        /\.(css|js|png|jpg|jpeg|gif|svg|woff|woff2|ttf|ico)$/i.test(pathname);
}

// Helper: Check if request is for HTML
function isHTMLPage(request) {
    return request.headers.get('accept')?.includes('text/html') ||
        request.mode === 'navigate';
}

// Helper: Check if external domain is allowed
function isAllowedExternal(hostname) {
    const allowed = ['fonts.googleapis.com', 'fonts.gstatic.com', 'cdnjs.cloudflare.com', 'unpkg.com'];
    return allowed.some(domain => hostname.includes(domain));
}

// Strategy 1: Cache First (for static assets - instant load)
async function cacheFirst(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cached = await cache.match(request);

        if (cached) {
            return cached;
        }

        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cache = await caches.open(STATIC_CACHE);
        return cache.match(request) || offlineResponse();
    }
}

// Strategy 2: Cache First with Background Update (for HTML pages)
async function cacheFirstWithUpdate(request) {
    const cache = await caches.open(PAGES_CACHE);
    const cached = await cache.match(request);

    // Return cached version immediately (fast!)
    if (cached) {
        // Update cache in background
        fetch(request)
            .then(response => {
                if (response.ok) {
                    cache.put(request, response.clone());
                }
            })
            .catch(err => console.log('[SW] Background update failed:', err));

        return cached;
    }

    // Not in cache, try network
    try {
        const response = await fetch(request);
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        console.error('[SW] Network failed, no cache:', error);
        return offlinePage();
    }
}

// Strategy 3: Network First (for dynamic content)
async function networkFirst(request) {
    try {
        const response = await fetch(request);

        if (response.ok) {
            const cache = await caches.open(RUNTIME_CACHE);
            cache.put(request, response.clone());
        }

        return response;
    } catch (error) {
        const cache = await caches.open(RUNTIME_CACHE);
        const cached = await cache.match(request);

        if (cached) {
            return cached;
        }

        // Check other caches as fallback
        const allCaches = await caches.keys();
        for (const cacheName of allCaches) {
            const cache = await caches.open(cacheName);
            const match = await cache.match(request);
            if (match) {
                return match;
            }
        }

        return offlineResponse();
    }
}

// Strategy 4: Cache First for External Resources
async function cacheFirstExternal(request) {
    try {
        const cache = await caches.open(STATIC_CACHE);
        const cached = await cache.match(request);

        if (cached) {
            return cached;
        }

        const response = await fetch(request, { mode: 'cors' });
        if (response.ok) {
            cache.put(request, response.clone());
        }
        return response;
    } catch (error) {
        const cache = await caches.open(STATIC_CACHE);
        return cache.match(request) || new Response('', { status: 503 });
    }
}

// Offline fallback page
function offlinePage() {
    return new Response(
        `<!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>AQUA - Offline</title>
            <style>
                * { margin: 0; padding: 0; box-sizing: border-box; }
                body {
                    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                    background: linear-gradient(135deg, #0b1120 0%, #1a2332 100%);
                    color: white;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    min-height: 100vh;
                    text-align: center;
                    padding: 2rem;
                }
                .container {
                    max-width: 400px;
                    animation: fadeIn 0.5s ease-in;
                }
                @keyframes fadeIn {
                    from { opacity: 0; transform: translateY(20px); }
                    to { opacity: 1; transform: translateY(0); }
                }
                h1 {
                    font-size: 5rem;
                    margin-bottom: 1rem;
                    animation: pulse 2s ease-in-out infinite;
                }
                @keyframes pulse {
                    0%, 100% { transform: scale(1); }
                    50% { transform: scale(1.1); }
                }
                h2 {
                    color: #00d2ff;
                    margin-bottom: 1rem;
                    font-size: 1.8rem;
                }
                p {
                    color: #cbd5e1;
                    line-height: 1.6;
                    margin-bottom: 2rem;
                    font-size: 1.1rem;
                }
                .status {
                    background: rgba(0, 210, 255, 0.1);
                    border: 2px solid #00d2ff;
                    border-radius: 12px;
                    padding: 1rem;
                    margin-bottom: 2rem;
                }
                button {
                    background: linear-gradient(135deg, #00d2ff, #3a7bd5);
                    border: none;
                    color: white;
                    padding: 1rem 2rem;
                    border-radius: 2rem;
                    font-size: 1rem;
                    font-weight: 700;
                    cursor: pointer;
                    box-shadow: 0 10px 30px rgba(0, 210, 255, 0.3);
                    transition: transform 0.2s;
                }
                button:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 15px 40px rgba(0, 210, 255, 0.4);
                }
                button:active {
                    transform: translateY(0);
                }
                .home-link {
                    display: inline-block;
                    margin-top: 1rem;
                    color: #00ff88;
                    text-decoration: none;
                    font-weight: 600;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>📡</h1>
                <h2>You're Offline</h2>
                <div class="status">
                    <p style="margin: 0;">⚠️ No internet connection detected</p>
                </div>
                <p>This page wasn't cached for offline use. Try going back to the home page or reconnect to the internet.</p>
                <button onclick="window.location.href='/'">🏠 Go Home</button>
                <button onclick="window.location.reload()" style="margin-left: 1rem; background: rgba(255,255,255,0.1);">🔄 Retry</button>
                <br>
                <a href="/" class="home-link">← Back to AQUA Home</a>
            </div>
        </body>
        </html>`,
        {
            status: 503,
            statusText: 'Service Unavailable',
            headers: { 'Content-Type': 'text/html' }
        }
    );
}

// Generic offline response
function offlineResponse() {
    return new Response(
        JSON.stringify({
            error: 'Offline',
            message: 'No internet connection and resource not cached',
            offline: true
        }),
        {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        }
    );
}

// Message handler
self.addEventListener('message', (event) => {
    if (event.data?.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }

    if (event.data?.type === 'CACHE_PAGES') {
        const urls = event.data.urls || [];
        caches.open(PAGES_CACHE).then(cache => {
            urls.forEach(url => {
                fetch(url).then(response => {
                    if (response.ok) {
                        cache.put(url, response);
                    }
                }).catch(err => console.log('[SW] Failed to cache:', url));
            });
        });
    }
});

console.log('[SW] ✅ AQUA Service Worker Ready - Full Offline Support Enabled');
