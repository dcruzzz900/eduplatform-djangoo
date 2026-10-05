/* EduPlatform Service Worker — cache shell + offline fallback */
const CACHE_VERSION = 'eduplatform-v1';
const SHELL = [
  '/',
  '/login/',
  '/offline/',
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/js/pwa.js',
  '/static/manifest.webmanifest',
  '/static/img/icon-192.svg',
  '/static/img/icon-512.svg',
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_VERSION).then((cache) => cache.addAll(SHELL)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE_VERSION).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (event) => {
  const req = event.request;
  if (req.method !== 'GET') return;

  const url = new URL(req.url);
  // Same-origin only
  if (url.origin !== self.location.origin) return;

  // Network-first for HTML navigations; cache-first for static assets
  if (req.mode === 'navigate' || (req.headers.get('accept') || '').includes('text/html')) {
    event.respondWith(networkFirst(req));
    return;
  }

  if (url.pathname.startsWith('/static/')) {
    event.respondWith(cacheFirst(req));
    return;
  }

  event.respondWith(networkFirst(req));
});

async function cacheFirst(req) {
  const cached = await caches.match(req);
  if (cached) return cached;
  try {
    const res = await fetch(req);
    const cache = await caches.open(CACHE_VERSION);
    cache.put(req, res.clone());
    return res;
  } catch {
    return caches.match('/offline/');
  }
}

async function networkFirst(req) {
  try {
    const res = await fetch(req);
    if (res && res.ok) {
      const cache = await caches.open(CACHE_VERSION);
      cache.put(req, res.clone());
    }
    return res;
  } catch {
    const cached = await caches.match(req);
    if (cached) return cached;
    return caches.match('/offline/');
  }
}

// Background sync hook for offline attendance queue (optional)
self.addEventListener('sync', (event) => {
  if (event.tag === 'attendance-sync') {
    event.waitUntil(Promise.resolve());
  }
});
