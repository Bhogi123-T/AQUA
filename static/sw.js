const CACHE_NAME = 'aquasphere-v2';
const ASSETS = [
    '/',
    '/static/style.css',
    '/static/main.js',
    '/static/offline-manager.js',
    '/static/manifest.json',
    '/static/logo.png',
    '/static/splash.png'
];

const API_CACHE = 'aquasphere-api-v1';
const DATASET_CACHE = 'aquasphere-datasets-v1';

self.addEventListener('install', (e) => {
    e.waitUntil(
        Promise.all([
            caches.open(CACHE_NAME).then((cache) => {
                return cache.addAll(ASSETS);
            }),
            caches.open(API_CACHE),
            caches.open(DATASET_CACHE)
        ])
    );
    self.skipWaiting();
});

self.addEventListener('activate', (e) => {
    e.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME && name !== API_CACHE && name !== DATASET_CACHE)
                    .map((name) => caches.delete(name))
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', (e) => {
    const url = new URL(e.request.url);

    // Cache static assets
    if (e.request.method === 'GET' && ASSETS.some(asset => url.pathname.includes(asset))) {
        e.respondWith(
            caches.match(e.request).then((response) => {
                return response || fetch(e.request).then((response) => {
                    const cache = caches.open(CACHE_NAME);
                    cache.then((c) => c.put(e.request, response.clone()));
                    return response;
                });
            }).catch(() => caches.match('/'))
        );
        return;
    }

    // Cache API responses for offline use
    if (url.pathname.includes('/api/dataset/') || url.pathname.includes('/market')) {
        e.respondWith(
            fetch(e.request)
                .then((response) => {
                    const cache = caches.open(DATASET_CACHE);
                    cache.then((c) => c.put(e.request, response.clone()));
                    return response;
                })
                .catch(() => caches.match(e.request))
        );
        return;
    }

    // Network first for dynamic content
    e.respondWith(
        fetch(e.request)
            .then((response) => {
                if (response.ok) {
                    const cache = caches.open(API_CACHE);
                    cache.then((c) => c.put(e.request, response.clone()));
                }
                return response;
            })
            .catch(() => caches.match(e.request))
    );
});
