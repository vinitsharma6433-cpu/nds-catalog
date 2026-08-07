// Minimal service worker - enables "Add to Home Screen" / Install prompt.
// Does not cache anything, so the catalog always loads fresh from GitHub.

self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // Pass-through - always fetch from network
  event.respondWith(fetch(event.request));
});
