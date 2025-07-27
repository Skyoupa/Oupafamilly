const CACHE_NAME = 'oupafamilly-elite-v1.0.0';
const OFFLINE_URL = '/offline.html';

// Ressources à mettre en cache immédiatement
const STATIC_CACHE_URLS = [
  '/',
  '/communaute',
  '/offline.html',
  '/manifest.json',
  '/icons/icon-192x192.png',
  '/icons/icon-512x512.png',
  // CSS et JS seront ajoutés dynamiquement
];

// URLs à mettre en cache lors de la navigation
const CACHE_ON_NAVIGATE = [
  '/tutoriels',
  '/admin',
  '/achievements'
];

// Installation du Service Worker
self.addEventListener('install', event => {
  console.log('🔧 SW: Installation en cours...');
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('🗄️ SW: Cache ouvert');
        return cache.addAll(STATIC_CACHE_URLS);
      })
      .then(() => {
        console.log('✅ SW: Ressources statiques mises en cache');
        return self.skipWaiting();
      })
      .catch(error => {
        console.error('❌ SW: Erreur installation:', error);
      })
  );
});

// Activation du Service Worker
self.addEventListener('activate', event => {
  console.log('🎯 SW: Activation en cours...');
  
  event.waitUntil(
    caches.keys()
      .then(cacheNames => {
        return Promise.all(
          cacheNames.map(cacheName => {
            if (cacheName !== CACHE_NAME) {
              console.log('🗑️ SW: Suppression ancien cache:', cacheName);
              return caches.delete(cacheName);
            }
          })
        );
      })
      .then(() => {
        console.log('✅ SW: Activation terminée');
        return self.clients.claim();
      })
  );
});

// Interception des requêtes (stratégie Cache First pour les assets, Network First pour l'API)
self.addEventListener('fetch', event => {
  const { request } = event;
  const url = new URL(request.url);
  
  // Ignorer les requêtes non-GET
  if (request.method !== 'GET') return;
  
  // Ignorer les requêtes chrome-extension et autres protocoles
  if (!url.protocol.startsWith('http')) return;
  
  // Stratégie pour les requêtes API (Network First)
  if (url.pathname.startsWith('/api/')) {
    event.respondWith(networkFirstStrategy(request));
    return;
  }
  
  // Stratégie pour les images et assets statiques (Cache First)
  if (request.destination === 'image' || 
      url.pathname.startsWith('/icons/') ||
      url.pathname.startsWith('/images/') ||
      request.destination === 'style' ||
      request.destination === 'script') {
    event.respondWith(cacheFirstStrategy(request));
    return;
  }
  
  // Stratégie pour les pages HTML (Stale While Revalidate)
  if (request.destination === 'document') {
    event.respondWith(staleWhileRevalidateStrategy(request));
    return;
  }
  
  // Stratégie par défaut (Network First)
  event.respondWith(networkFirstStrategy(request));
});

// Stratégie Cache First (pour les assets statiques)
async function cacheFirstStrategy(request) {
  try {
    const cache = await caches.open(CACHE_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      console.log('📦 SW: Servi depuis le cache:', request.url);
      return cachedResponse;
    }
    
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
    
  } catch (error) {
    console.log('❌ SW: Erreur Cache First:', error);
    return new Response('Ressource indisponible', { status: 404 });
  }
}

// Stratégie Network First (pour l'API et contenu dynamique)
async function networkFirstStrategy(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_NAME);
      cache.put(request, networkResponse.clone());
    }
    
    return networkResponse;
    
  } catch (error) {
    console.log('🔄 SW: Network failed, trying cache for:', request.url);
    
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Si c'est une requête API, retourner une réponse offline
    if (request.url.includes('/api/')) {
      return new Response(
        JSON.stringify({ 
          error: 'Connexion hors ligne', 
          offline: true,
          message: 'Vous semblez être hors ligne. Certaines fonctionnalités peuvent être indisponibles.'
        }), 
        {
          status: 503,
          headers: { 'Content-Type': 'application/json' }
        }
      );
    }
    
    // Pour les pages, rediriger vers la page offline
    if (request.destination === 'document') {
      return caches.match(OFFLINE_URL) || new Response('Page hors ligne indisponible');
    }
    
    return new Response('Contenu indisponible hors ligne', { status: 503 });
  }
}

// Stratégie Stale While Revalidate (pour les pages HTML)
async function staleWhileRevalidateStrategy(request) {
  const cache = await caches.open(CACHE_NAME);
  const cachedResponse = await cache.match(request);
  
  const fetchPromise = fetch(request).then(networkResponse => {
    if (networkResponse.ok) {
      cache.put(request, networkResponse.clone());
    }
    return networkResponse;
  }).catch(() => cachedResponse);
  
  return cachedResponse || fetchPromise;
}

// Synchronisation en arrière-plan
self.addEventListener('sync', event => {
  console.log('🔄 SW: Synchronisation en arrière-plan:', event.tag);
  
  if (event.tag === 'background-sync') {
    event.waitUntil(
      // Ici on peut synchroniser les données en attente
      syncPendingData()
    );
  }
});

async function syncPendingData() {
  // Récupérer les données en attente depuis IndexedDB
  // Les envoyer vers l'API quand la connexion est rétablie
  console.log('📡 SW: Synchronisation des données...');
}

// Notifications Push
self.addEventListener('push', event => {
  console.log('📱 SW: Notification push reçue');
  
  const options = {
    body: event.data ? event.data.text() : 'Nouvelle notification Oupafamilly !',
    icon: '/icons/icon-192x192.png',
    badge: '/icons/icon-72x72.png',
    vibrate: [100, 50, 100],
    data: {
      dateOfArrival: Date.now(),
      primaryKey: '2'
    },
    actions: [
      {
        action: 'explore',
        title: 'Voir',
        icon: '/icons/icon-72x72.png'
      },
      {
        action: 'close',
        title: 'Fermer',
        icon: '/icons/icon-72x72.png'
      }
    ]
  };
  
  event.waitUntil(
    self.registration.showNotification('Oupafamilly', options)
  );
});

// Gestion des clics sur notifications
self.addEventListener('notificationclick', event => {
  console.log('🔔 SW: Clic sur notification:', event.action);
  
  event.notification.close();
  
  if (event.action === 'explore') {
    event.waitUntil(
      clients.openWindow('/communaute')
    );
  }
});

// Message du client vers le Service Worker
self.addEventListener('message', event => {
  console.log('💬 SW: Message reçu:', event.data);
  
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting();
  }
  
  // Répondre au client
  event.ports[0].postMessage({
    type: 'SW_READY',
    message: 'Service Worker opérationnel !'
  });
});

console.log('🚀 Oupafamilly Service Worker v1.0.0 chargé !');