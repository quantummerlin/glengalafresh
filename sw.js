const CACHE_NAME = 'glengala-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/shop.html',
  '/about.html',
  '/science.html',
  '/contact.html',
  '/blog.html',
  '/partnerships.html',
  '/products/beetroid.html',
  '/products/immuni-tea.html',
  '/products/immuni-fire.html',
  '/products/golden-fire.html',
  '/products/celery.html',
  '/articles/beetroot-daily.html',
  '/articles/celery-challenge.html',
  '/articles/golden-fire-science.html',
  '/articles/ozonated-water-truth.html',
  '/articles/turmeric-cayenne.html',
  '/css/style.css',
  '/js/main.js',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', event => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    caches.match(event.request).then(cached => {
      if (cached) return cached;
      return fetch(event.request).then(response => {
        if (!response || response.status !== 200 || response.type === 'opaque') return response;
        const clone = response.clone();
        caches.open(CACHE_NAME).then(cache => cache.put(event.request, clone));
        return response;
      });
    }).catch(() => caches.match('/index.html'))
  );
});
