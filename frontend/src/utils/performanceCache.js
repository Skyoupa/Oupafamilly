/**
 * 🚀 PERFORMANCE CACHE MANAGER - ÉLITE SYSTEM
 * Système de cache intelligent pour Oupafamilly
 */

import React from 'react';

class PerformanceCacheManager {
  constructor() {
    this.memoryCache = new Map();
    this.cacheTTL = {
      'api_achievements': 5 * 60 * 1000,      // 5 minutes
      'api_tournaments': 2 * 60 * 1000,       // 2 minutes  
      'api_leaderboard': 30 * 1000,           // 30 secondes
      'api_community': 1 * 60 * 1000,         // 1 minute
      'static_content': 30 * 60 * 1000,       // 30 minutes
      'user_profile': 5 * 60 * 1000,          // 5 minutes
      'default': 1 * 60 * 1000                // 1 minute par défaut
    };
    
    this.maxCacheSize = 100; // Maximum d'entrées en cache
    this.stats = {
      hits: 0,
      misses: 0,
      evictions: 0
    };
    
    // Nettoyer le cache expiré toutes les minutes
    setInterval(() => this.cleanup(), 60 * 1000);
    
    console.log('🚀 PerformanceCacheManager initialisé');
  }

  /**
   * Génère une clé de cache basée sur l'URL et les paramètres
   */
  generateKey(url, params = {}) {
    const paramsString = Object.keys(params)
      .sort()
      .map(key => `${key}=${params[key]}`)
      .join('&');
    
    return `${url}${paramsString ? '?' + paramsString : ''}`;
  }

  /**
   * Détermine le TTL basé sur le type de requête
   */
  getTTL(url) {
    if (url.includes('/api/achievements')) return this.cacheTTL.api_achievements;
    if (url.includes('/api/tournaments')) return this.cacheTTL.api_tournaments;
    if (url.includes('/api/elo')) return this.cacheTTL.api_leaderboard;
    if (url.includes('/api/community')) return this.cacheTTL.api_community;
    if (url.includes('/api/')) return this.cacheTTL.default;
    return this.cacheTTL.static_content;
  }

  /**
   * Met en cache une réponse
   */
  set(key, data, customTTL = null) {
    try {
      // Vérifier la taille du cache
      if (this.memoryCache.size >= this.maxCacheSize) {
        this.evictOldest();
      }

      const ttl = customTTL || this.getTTL(key);
      const expiresAt = Date.now() + ttl;
      
      const cacheEntry = {
        data: this.deepClone(data),
        expiresAt,
        lastAccessed: Date.now(),
        hitCount: 0
      };

      this.memoryCache.set(key, cacheEntry);
      console.log(`📦 Cache SET: ${key} (TTL: ${ttl}ms)`);
      
    } catch (error) {
      console.error('❌ Erreur cache SET:', error);
    }
  }

  /**
   * Récupère une donnée du cache
   */
  get(key) {
    try {
      const entry = this.memoryCache.get(key);
      
      if (!entry) {
        this.stats.misses++;
        console.log(`🔍 Cache MISS: ${key}`);
        return null;
      }

      // Vérifier l'expiration
      if (Date.now() > entry.expiresAt) {
        this.memoryCache.delete(key);
        this.stats.misses++;
        console.log(`⏰ Cache EXPIRED: ${key}`);
        return null;
      }

      // Mettre à jour les statistiques d'accès
      entry.lastAccessed = Date.now();
      entry.hitCount++;
      this.stats.hits++;
      
      console.log(`✅ Cache HIT: ${key} (hits: ${entry.hitCount})`);
      return this.deepClone(entry.data);
      
    } catch (error) {
      console.error('❌ Erreur cache GET:', error);
      this.stats.misses++;
      return null;
    }
  }

  /**
   * Supprime une entrée du cache
   */
  delete(key) {
    const deleted = this.memoryCache.delete(key);
    if (deleted) {
      console.log(`🗑️ Cache DELETE: ${key}`);
    }
    return deleted;
  }

  /**
   * Invalide le cache par pattern
   */
  invalidatePattern(pattern) {
    let deletedCount = 0;
    for (const key of this.memoryCache.keys()) {
      if (key.includes(pattern)) {
        this.memoryCache.delete(key);
        deletedCount++;
      }
    }
    console.log(`🔄 Cache INVALIDATE PATTERN: ${pattern} (${deletedCount} entrées)`);
    return deletedCount;
  }

  /**
   * Nettoie les entrées expirées
   */
  cleanup() {
    const now = Date.now();
    let cleanedCount = 0;
    
    for (const [key, entry] of this.memoryCache.entries()) {
      if (now > entry.expiresAt) {
        this.memoryCache.delete(key);
        cleanedCount++;
      }
    }
    
    if (cleanedCount > 0) {
      console.log(`🧹 Cache CLEANUP: ${cleanedCount} entrées expirées supprimées`);
    }
  }

  /**
   * Évince l'entrée la plus ancienne (LRU)
   */
  evictOldest() {
    let oldestKey = null;
    let oldestTime = Date.now();
    
    for (const [key, entry] of this.memoryCache.entries()) {
      if (entry.lastAccessed < oldestTime) {
        oldestTime = entry.lastAccessed;
        oldestKey = key;
      }
    }
    
    if (oldestKey) {
      this.memoryCache.delete(oldestKey);
      this.stats.evictions++;
      console.log(`📤 Cache EVICT: ${oldestKey}`);
    }
  }

  /**
   * Clone profond pour éviter les mutations
   */
  deepClone(obj) {
    try {
      return JSON.parse(JSON.stringify(obj));
    } catch (error) {
      console.warn('⚠️ Erreur deep clone, retour original:', error);
      return obj;
    }
  }

  /**
   * Statistiques du cache
   */
  getStats() {
    const hitRate = this.stats.hits + this.stats.misses > 0 
      ? ((this.stats.hits / (this.stats.hits + this.stats.misses)) * 100).toFixed(2)
      : 0;

    return {
      ...this.stats,
      hitRate: `${hitRate}%`,
      size: this.memoryCache.size,
      maxSize: this.maxCacheSize
    };
  }

  /**
   * Vide complètement le cache
   */
  clear() {
    const size = this.memoryCache.size;
    this.memoryCache.clear();
    console.log(`🗑️ Cache CLEAR: ${size} entrées supprimées`);
  }

  /**
   * Préchargement intelligent
   */
  async preload(urls) {
    console.log('🔄 Cache PRELOAD commencé...');
    
    const promises = urls.map(async (url) => {
      try {
        const response = await fetch(url);
        if (response.ok) {
          const data = await response.json();
          this.set(url, data);
        }
      } catch (error) {
        console.warn(`⚠️ Erreur preload ${url}:`, error);
      }
    });
    
    await Promise.allSettled(promises);
    console.log('✅ Cache PRELOAD terminé');
  }
}

// Instance globale
const cacheManager = new PerformanceCacheManager();

/**
 * 🚀 FETCH WRAPPER AVEC CACHE INTELLIGENT
 */
export const cachedFetch = async (url, options = {}) => {
  // Clé de cache basée sur l'URL et les options
  const cacheKey = cacheManager.generateKey(url, options.params || {});
  
  // Vérifier le cache pour les requêtes GET
  if (!options.method || options.method === 'GET') {
    const cachedData = cacheManager.get(cacheKey);
    if (cachedData) {
      return Promise.resolve({
        ok: true,
        json: () => Promise.resolve(cachedData),
        fromCache: true
      });
    }
  }

  try {
    // Faire la requête réseau
    const response = await fetch(url, options);
    
    if (response.ok && (!options.method || options.method === 'GET')) {
      const data = await response.json();
      cacheManager.set(cacheKey, data);
      
      return {
        ...response,
        json: () => Promise.resolve(data),
        fromCache: false
      };
    }
    
    return response;
    
  } catch (error) {
    // En cas d'erreur réseau, essayer le cache
    if (!options.method || options.method === 'GET') {
      const cachedData = cacheManager.get(cacheKey);
      if (cachedData) {
        console.log('🔄 Utilisation cache suite à erreur réseau');
        return {
          ok: true,
          json: () => Promise.resolve(cachedData),
          fromCache: true,
          fromError: true
        };
      }
    }
    
    throw error;
  }
};

/**
 * 🚀 HOOK REACT POUR CACHE STATS
 */
export const useCacheStats = () => {
  const [stats, setStats] = React.useState(cacheManager.getStats());
  
  React.useEffect(() => {
    const interval = setInterval(() => {
      setStats(cacheManager.getStats());
    }, 5000); // Mise à jour toutes les 5 secondes
    
    return () => clearInterval(interval);
  }, []);
  
  return stats;
};

/**
 * 🚀 INVALIDATION HOOKS POUR MUTATIONS
 */
export const useCacheInvalidation = () => {
  return {
    invalidateAchievements: () => cacheManager.invalidatePattern('/api/achievements'),
    invalidateTournaments: () => cacheManager.invalidatePattern('/api/tournaments'),
    invalidateLeaderboard: () => cacheManager.invalidatePattern('/api/elo'),
    invalidateCommunity: () => cacheManager.invalidatePattern('/api/community'),
    invalidateAll: () => cacheManager.clear()
  };
};

/**
 * 🚀 PRELOAD POUR PAGES IMPORTANTES
 */
export const preloadEssentialData = async () => {
  const essentialUrls = [
    '/api/achievements/available',
    '/api/achievements/my-badges',
    '/api/elo/leaderboard',
    '/api/tournaments/current'
  ];
  
  await cacheManager.preload(essentialUrls);
};

// Export du cache manager pour usage avancé
export { cacheManager };

console.log('🚀 Performance Cache System chargé!');