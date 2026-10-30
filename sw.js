/* ==============================================================================
   DBYC PWA SERVICE WORKER (Don Bosco Youth Centre - Basin Bridge, Chennai)
   High-Performance Offline App Shell & Smart Cache Engine
   ============================================================================== */

const CACHE_NAME = 'dbyc-portal-v2.0';
const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './assets/logo.png',
  './assets/don_bosco.webp',
  './assets/icon-192.png',
  './assets/icon-512.png',
  './assets/dbyc_seal.png',
  './assets/director_signature.png'
];

// 1. Install & Cache App Shell
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS).catch((err) => {
        console.warn('[DBYC SW] Optional asset cache warning:', err);
      });
    })
  );
  self.skipWaiting();
});

// 2. Activate & Purge Stale Caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            console.log('[DBYC SW] Removing old cache:', key);
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// 3. Fetch Strategy: Network-First for HTML/Cloud, Cache-First for Assets
self.addEventListener('fetch', (event) => {
  const req = event.request;
  const url = new URL(req.url);

  // Bypass Google Apps Script & external cloud APIs (always live network)
  if (url.hostname.includes('script.google.com') || url.hostname.includes('googleusercontent.com') || req.method !== 'GET') {
    return;
  }

  // Network-First for index.html / app root navigation
  if (req.mode === 'navigate' || url.pathname.endsWith('index.html') || url.pathname === '/' || url.pathname === '') {
    event.respondWith(
      fetch(req)
        .then((networkRes) => {
          if (networkRes && networkRes.status === 200) {
            const resClone = networkRes.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
          }
          return networkRes;
        })
        .catch(() => {
          return caches.match(req).then((cached) => cached || caches.match('./index.html'));
        })
    );
    return;
  }

  // Cache-First for static assets (images, icons, fonts)
  event.respondWith(
    caches.match(req).then((cachedRes) => {
      if (cachedRes) {
        return cachedRes;
      }
      return fetch(req).then((networkRes) => {
        if (networkRes && networkRes.status === 200) {
          const resClone = networkRes.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(req, resClone));
        }
        return networkRes;
      }).catch(() => {
        // Fallback for missing offline image if needed
        return null;
      });
    })
  );
});
