"""
Redis Cache Configuration and Utilities
"""

import redis
import json
import os
import logging
from functools import wraps
from typing import Any, Optional, Union
from datetime import timedelta
import asyncio
import pickle

logger = logging.getLogger(__name__)

class RedisCache:
    """Redis cache manager with async support"""
    
    def __init__(self):
        self.redis_url = os.environ.get('REDIS_URL', 'redis://localhost:6379/0')
        self.default_ttl = int(os.environ.get('CACHE_DEFAULT_TTL', '300'))  # 5 minutes
        self.enabled = os.environ.get('CACHE_ENABLED', 'true').lower() == 'true'
        
        if self.enabled:
            try:
                self.client = redis.from_url(
                    self.redis_url,
                    decode_responses=True,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                    retry_on_timeout=True
                )
                # Test connection
                self.client.ping()
                logger.info("✅ Redis cache connected successfully")
            except Exception as e:
                logger.warning(f"⚠️ Redis connection failed: {str(e)}. Cache disabled.")
                self.enabled = False
                self.client = None
        else:
            logger.info("📝 Redis cache disabled via configuration")
            self.client = None
    
    def _serialize_key(self, key: str, prefix: str = "oupafamilly") -> str:
        """Generate cache key with prefix"""
        return f"{prefix}:{key}"
    
    def _serialize_value(self, value: Any) -> str:
        """Serialize value for storage"""
        try:
            if isinstance(value, (dict, list, tuple)):
                return json.dumps(value, default=str)
            return str(value)
        except Exception as e:
            logger.error(f"Cache serialization error: {str(e)}")
            return str(value)
    
    def _deserialize_value(self, value: str) -> Any:
        """Deserialize value from storage"""
        try:
            # Try JSON first
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            # Return as string if JSON fails
            return value
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set cache value with optional TTL"""
        if not self.enabled or not self.client:
            return False
        
        try:
            cache_key = self._serialize_key(key)
            serialized_value = self._serialize_value(value)
            ttl = ttl or self.default_ttl
            
            result = self.client.setex(cache_key, ttl, serialized_value)
            logger.debug(f"Cache SET: {cache_key} (TTL: {ttl}s)")
            return result
        except Exception as e:
            logger.error(f"Cache SET error: {str(e)}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """Get cache value"""
        if not self.enabled or not self.client:
            return None
        
        try:
            cache_key = self._serialize_key(key)
            value = self.client.get(cache_key)
            
            if value is None:
                logger.debug(f"Cache MISS: {cache_key}")
                return None
            
            logger.debug(f"Cache HIT: {cache_key}")
            return self._deserialize_value(value)
        except Exception as e:
            logger.error(f"Cache GET error: {str(e)}")
            return None
    
    def delete(self, key: str) -> bool:
        """Delete cache value"""
        if not self.enabled or not self.client:
            return False
        
        try:
            cache_key = self._serialize_key(key)
            result = self.client.delete(cache_key)
            logger.debug(f"Cache DELETE: {cache_key}")
            return bool(result)
        except Exception as e:
            logger.error(f"Cache DELETE error: {str(e)}")
            return False
    
    def delete_pattern(self, pattern: str) -> int:
        """Delete multiple keys matching pattern"""
        if not self.enabled or not self.client:
            return 0
        
        try:
            pattern_key = self._serialize_key(pattern)
            keys = self.client.keys(pattern_key)
            if keys:
                result = self.client.delete(*keys)
                logger.debug(f"Cache DELETE PATTERN: {pattern} ({result} keys)")
                return result
            return 0
        except Exception as e:
            logger.error(f"Cache DELETE PATTERN error: {str(e)}")
            return 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if not self.enabled or not self.client:
            return False
        
        try:
            cache_key = self._serialize_key(key)
            return bool(self.client.exists(cache_key))
        except Exception as e:
            logger.error(f"Cache EXISTS error: {str(e)}")
            return False
    
    def clear_all(self) -> bool:
        """Clear all cache (development only)"""
        if not self.enabled or not self.client:
            return False
        
        try:
            # Only clear keys with our prefix
            keys = self.client.keys("oupafamilly:*")
            if keys:
                result = self.client.delete(*keys)
                logger.info(f"Cache CLEARED: {result} keys removed")
                return True
            return True
        except Exception as e:
            logger.error(f"Cache CLEAR error: {str(e)}")
            return False

# Global cache instance
cache = RedisCache()

def cached(ttl: int = 300, key_prefix: str = ""):
    """
    Decorator for caching function results
    
    Args:
        ttl: Time to live in seconds (default: 5 minutes)
        key_prefix: Optional prefix for cache key
    """
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Generate cache key from function name and parameters
            func_name = f"{func.__module__}.{func.__name__}"
            args_key = "_".join(str(arg) for arg in args if isinstance(arg, (str, int, float)))
            kwargs_key = "_".join(f"{k}_{v}" for k, v in sorted(kwargs.items()) if isinstance(v, (str, int, float)))
            
            cache_key = f"{key_prefix}_{func_name}_{args_key}_{kwargs_key}".strip("_")
            
            # Try to get from cache first
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"🎯 Cache hit for {func_name}")
                return cached_result
            
            # Execute function and cache result
            logger.debug(f"🔄 Cache miss for {func_name}, executing...")
            result = await func(*args, **kwargs) if asyncio.iscoroutinefunction(func) else func(*args, **kwargs)
            
            # Cache the result
            cache.set(cache_key, result, ttl)
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Same logic for synchronous functions
            func_name = f"{func.__module__}.{func.__name__}"
            args_key = "_".join(str(arg) for arg in args if isinstance(arg, (str, int, float)))
            kwargs_key = "_".join(f"{k}_{v}" for k, v in sorted(kwargs.items()) if isinstance(v, (str, int, float)))
            
            cache_key = f"{key_prefix}_{func_name}_{args_key}_{kwargs_key}".strip("_")
            
            cached_result = cache.get(cache_key)
            if cached_result is not None:
                logger.debug(f"🎯 Cache hit for {func_name}")
                return cached_result
            
            logger.debug(f"🔄 Cache miss for {func_name}, executing...")
            result = func(*args, **kwargs)
            cache.set(cache_key, result, ttl)
            return result
        
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Cache invalidation utilities
class CacheInvalidator:
    """Utilities for cache invalidation"""
    
    @staticmethod
    def invalidate_user_cache(user_id: str):
        """Invalidate all cache entries for a specific user"""
        cache.delete_pattern(f"*user_{user_id}*")
        logger.info(f"🗑️ Invalidated cache for user {user_id}")
    
    @staticmethod
    def invalidate_tournament_cache(tournament_id: str = None):
        """Invalidate tournament-related cache"""
        if tournament_id:
            cache.delete_pattern(f"*tournament_{tournament_id}*")
            logger.info(f"🗑️ Invalidated cache for tournament {tournament_id}")
        else:
            cache.delete_pattern("*tournament*")
            logger.info("🗑️ Invalidated all tournament cache")
    
    @staticmethod
    def invalidate_community_cache():
        """Invalidate community-related cache (leaderboards, stats, etc.)"""
        cache.delete_pattern("*community*")
        cache.delete_pattern("*leaderboard*")
        cache.delete_pattern("*stats*")
        logger.info("🗑️ Invalidated community cache")

# Export cache utilities
invalidate = CacheInvalidator()