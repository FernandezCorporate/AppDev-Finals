// ⚠️ Bump this version string every time you update CSS/JS files.
// Changing it forces all users to get a fresh cache immediately.
const CACHE_NAME = 'site-scheduler-v2';

// Install: pre-cache core assets with the CORRECT paths
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll([
                '/',
                '/static/css/main.css',         // ✅ Fixed path (was /static/main.css)
                '/static/js/bootstrap.bundle.min.js',
                '/static/css/bootstrap.min.css',
            ]);
        })
    );
    // Force the new SW to activate immediately, don't wait for old one to die
    self.skipWaiting();
});

// Activate: delete ALL old caches so stale CSS/JS is wiped out
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames
                    .filter((name) => name !== CACHE_NAME) // keep only current version
                    .map((name) => {
                        console.log('[SW] Deleting old cache:', name);
                        return caches.delete(name);
                    })
            );
        }).then(() => {
            // Take control of all open tabs immediately
            return self.clients.claim();
        })
    );
});

// Fetch: Network-First for HTML pages, Cache-First for static assets
self.addEventListener('fetch', (event) => {
    if (event.request.method !== 'GET') return;

    const url = new URL(event.request.url);
    const isStaticAsset = url.pathname.startsWith('/static/');

    if (isStaticAsset) {
        // Cache-First for CSS/JS/images — fast, and version bump handles updates
        event.respondWith(
            caches.match(event.request).then((cached) => {
                return cached || fetch(event.request).then((networkResponse) => {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                });
            })
        );
    } else {
        // Network-First for HTML pages — always fresh content from Django
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    return caches.open(CACHE_NAME).then((cache) => {
                        cache.put(event.request, networkResponse.clone());
                        return networkResponse;
                    });
                })
                .catch(() => {
                    // Offline fallback
                    return caches.match(event.request);
                })
        );
    }
});