"""
Cache utilities for SBOMAI.
"""

import asyncio
import json
import time
from typing import Any, Optional, Dict
import logging
from ..config import get_config
from .monitoring import record_cache_hit, record_cache_miss, update_cache_size

logger = logging.getLogger(__name__)

class Cache:
    """
    Simple in-memory cache with TTL support.
    """
    
    def __init__(self):
        self.config = get_config()
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._cache_type = self.config.cache_type
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if key in self._cache:
            entry = self._cache[key]
            
            # Check if expired
            if time.time() > entry['expires_at']:
                del self._cache[key]
                record_cache_miss(self._cache_type)
                return None
            
            # Record hit
            record_cache_hit(self._cache_type)
            return entry['value']
        
        # Record miss
        record_cache_miss(self._cache_type)
        return None
    
    async def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache with TTL"""
        if ttl is None:
            ttl = self.config.cache_ttl
        
        self._cache[key] = {
            'value': value,
            'expires_at': time.time() + ttl
        }
        
        # Update cache size metric
        cache_size = len(json.dumps(self._cache).encode('utf-8'))
        update_cache_size(self._cache_type, cache_size)
    
    async def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if key in self._cache:
            del self._cache[key]
            return True
        return False
    
    async def clear(self) -> None:
        """Clear all cache entries"""
        self._cache.clear()
        update_cache_size(self._cache_type, 0)
    
    async def keys(self) -> list:
        """Get all cache keys"""
        return list(self._cache.keys())
    
    async def size(self) -> int:
        """Get cache size"""
        return len(self._cache)
    
    async def cleanup_expired(self) -> int:
        """Remove expired entries and return count"""
        now = time.time()
        expired_keys = [
            key for key, entry in self._cache.items()
            if now > entry['expires_at']
        ]
        
        for key in expired_keys:
            del self._cache[key]
        
        return len(expired_keys) 