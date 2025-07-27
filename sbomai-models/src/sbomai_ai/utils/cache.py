"""
Caching utilities for SBOMAI AI Microservice
"""

import logging
import time
import hashlib
import json
from typing import Any, Optional, Dict, List
from functools import wraps
import pickle
import os
from datetime import datetime, timedelta

from ..config import get_config
from .monitoring import CacheMonitor

logger = logging.getLogger(__name__)


class Cache:
    """Base cache class"""
    
    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self.cache_monitor = CacheMonitor()
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        raise NotImplementedError
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        raise NotImplementedError
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        raise NotImplementedError
    
    def clear(self) -> None:
        """Clear all cache entries"""
        raise NotImplementedError
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        raise NotImplementedError


class MemoryCache(Cache):
    """In-memory cache implementation"""
    
    def __init__(self, ttl: int = 3600, max_size: int = 1000):
        super().__init__(ttl)
        self.max_size = max_size
        self._cache: Dict[str, Dict[str, Any]] = {}
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key not in self._cache:
            self.cache_monitor.record_cache_miss("memory")
            return None
        
        entry = self._cache[key]
        if time.time() > entry['expires_at']:
            del self._cache[key]
            self.cache_monitor.record_cache_miss("memory")
            return None
        
        self.cache_monitor.record_cache_hit("memory")
        return entry['value']
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        # Evict oldest entries if cache is full
        if len(self._cache) >= self.max_size:
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k]['expires_at'])
            del self._cache[oldest_key]
        
        self._cache[key] = {
            'value': value,
            'expires_at': time.time() + self.ttl
        }
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        if key in self._cache:
            del self._cache[key]
    
    def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        if key not in self._cache:
            return False
        
        if time.time() > self._cache[key]['expires_at']:
            del self._cache[key]
            return False
        
        return True
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        return {
            "size": len(self._cache),
            "max_size": self.max_size,
            "hit_rate": self.cache_monitor.get_cache_hit_rate("memory"),
            "ttl": self.ttl
        }


class FileCache(Cache):
    """File-based cache implementation"""
    
    def __init__(self, cache_dir: str, ttl: int = 3600):
        super().__init__(ttl)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def _get_cache_path(self, key: str) -> str:
        """Get cache file path for key"""
        # Create a safe filename from the key
        safe_key = hashlib.md5(key.encode()).hexdigest()
        return os.path.join(self.cache_dir, f"{safe_key}.cache")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        cache_path = self._get_cache_path(key)
        
        if not os.path.exists(cache_path):
            self.cache_monitor.record_cache_miss("file")
            return None
        
        try:
            with open(cache_path, 'rb') as f:
                entry = pickle.load(f)
            
            if time.time() > entry['expires_at']:
                os.remove(cache_path)
                self.cache_monitor.record_cache_miss("file")
                return None
            
            self.cache_monitor.record_cache_hit("file")
            return entry['value']
            
        except Exception as e:
            logger.error(f"Error reading cache file {cache_path}: {e}")
            self.cache_monitor.record_cache_miss("file")
            return None
    
    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        cache_path = self._get_cache_path(key)
        
        try:
            entry = {
                'value': value,
                'expires_at': time.time() + self.ttl,
                'created_at': time.time()
            }
            
            with open(cache_path, 'wb') as f:
                pickle.dump(entry, f)
                
        except Exception as e:
            logger.error(f"Error writing cache file {cache_path}: {e}")
    
    def delete(self, key: str) -> None:
        """Delete value from cache"""
        cache_path = self._get_cache_path(key)
        if os.path.exists(cache_path):
            os.remove(cache_path)
    
    def clear(self) -> None:
        """Clear all cache entries"""
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.cache'):
                os.remove(os.path.join(self.cache_dir, filename))
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache"""
        cache_path = self._get_cache_path(key)
        if not os.path.exists(cache_path):
            return False
        
        try:
            with open(cache_path, 'rb') as f:
                entry = pickle.load(f)
            
            if time.time() > entry['expires_at']:
                os.remove(cache_path)
                return False
            
            return True
            
        except Exception:
            return False
    
    def cleanup_expired(self) -> int:
        """Clean up expired cache entries"""
        cleaned = 0
        current_time = time.time()
        
        for filename in os.listdir(self.cache_dir):
            if filename.endswith('.cache'):
                cache_path = os.path.join(self.cache_dir, filename)
                try:
                    with open(cache_path, 'rb') as f:
                        entry = pickle.load(f)
                    
                    if current_time > entry['expires_at']:
                        os.remove(cache_path)
                        cleaned += 1
                        
                except Exception as e:
                    logger.error(f"Error cleaning up cache file {cache_path}: {e}")
                    # Remove corrupted cache files
                    os.remove(cache_path)
                    cleaned += 1
        
        return cleaned
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics"""
        total_files = len([f for f in os.listdir(self.cache_dir) if f.endswith('.cache')])
        return {
            "total_files": total_files,
            "cache_dir": self.cache_dir,
            "hit_rate": self.cache_monitor.get_cache_hit_rate("file"),
            "ttl": self.ttl
        }


class CacheManager:
    """Manages multiple cache instances"""
    
    def __init__(self):
        self.config = get_config()
        self.caches: Dict[str, Cache] = {}
        self._setup_caches()
    
    def _setup_caches(self):
        """Setup cache instances"""
        # Memory cache for fast access
        self.caches['memory'] = MemoryCache(
            ttl=self.config.service.cache_ttl,
            max_size=1000
        )
        
        # File cache for persistent storage
        file_cache_dir = os.path.join(self.config.data.cache_dir, 'ai_cache')
        self.caches['file'] = FileCache(
            cache_dir=file_cache_dir,
            ttl=self.config.service.cache_ttl
        )
    
    def get(self, cache_type: str, key: str) -> Optional[Any]:
        """Get value from specified cache"""
        if cache_type not in self.caches:
            logger.warning(f"Unknown cache type: {cache_type}")
            return None
        
        return self.caches[cache_type].get(key)
    
    def set(self, cache_type: str, key: str, value: Any) -> None:
        """Set value in specified cache"""
        if cache_type not in self.caches:
            logger.warning(f"Unknown cache type: {cache_type}")
            return
        
        self.caches[cache_type].set(key, value)
    
    def delete(self, cache_type: str, key: str) -> None:
        """Delete value from specified cache"""
        if cache_type not in self.caches:
            logger.warning(f"Unknown cache type: {cache_type}")
            return
        
        self.caches[cache_type].delete(key)
    
    def clear(self, cache_type: str = None) -> None:
        """Clear cache(s)"""
        if cache_type:
            if cache_type in self.caches:
                self.caches[cache_type].clear()
        else:
            for cache in self.caches.values():
                cache.clear()
    
    def get_stats(self) -> Dict[str, Any]:
        """Get statistics for all caches"""
        stats = {}
        for cache_type, cache in self.caches.items():
            stats[cache_type] = cache.get_stats()
        return stats
    
    def cleanup(self) -> None:
        """Clean up expired entries in all caches"""
        for cache_type, cache in self.caches.items():
            if hasattr(cache, 'cleanup_expired'):
                cleaned = cache.cleanup_expired()
                if cleaned > 0:
                    logger.info(f"Cleaned up {cleaned} expired entries from {cache_type} cache")


def cache_result(cache_type: str = "memory", ttl: int = None, key_prefix: str = ""):
    """Decorator to cache function results"""
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cache_manager = CacheManager()
            
            # Generate cache key
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix)
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_type, cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = await func(*args, **kwargs)
            
            # Cache result
            cache_ttl = ttl or get_config().service.cache_ttl
            cache_manager.caches[cache_type].ttl = cache_ttl
            cache_manager.set(cache_type, cache_key, result)
            
            return result
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cache_manager = CacheManager()
            
            # Generate cache key
            cache_key = _generate_cache_key(func, args, kwargs, key_prefix)
            
            # Try to get from cache
            cached_result = cache_manager.get(cache_type, cache_key)
            if cached_result is not None:
                return cached_result
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache result
            cache_ttl = ttl or get_config().service.cache_ttl
            cache_manager.caches[cache_type].ttl = cache_ttl
            cache_manager.set(cache_type, cache_key, result)
            
            return result
        
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper
    
    return decorator


def _generate_cache_key(func, args, kwargs, prefix: str) -> str:
    """Generate cache key from function call"""
    # Create a unique key based on function name, args, and kwargs
    key_data = {
        'func_name': func.__name__,
        'args': args,
        'kwargs': kwargs
    }
    
    key_string = json.dumps(key_data, sort_keys=True, default=str)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    
    return f"{prefix}:{key_hash}" if prefix else key_hash


# Global cache manager instance
_cache_manager = None

def get_cache_manager() -> CacheManager:
    """Get global cache manager instance"""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager 


    