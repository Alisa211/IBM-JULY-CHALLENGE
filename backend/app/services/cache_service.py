import logging
import hashlib
from typing import Optional, Any

logger = logging.getLogger(__name__)

class CacheService:
    """Service to handle caching, primarily to prevent blowing out API limits (e.g., Discovery)."""
    
    def __init__(self):
        # Fallback to simple dict if Redis isn't configured in local env
        self._local_cache = {}

    def _generate_key(self, namespace: str, text: str) -> str:
        h = hashlib.md5(text.encode("utf-8")).hexdigest()
        return f"{namespace}:{h}"

    async def get(self, namespace: str, key_text: str) -> Optional[Any]:
        """Retrieve value from cache."""
        key = self._generate_key(namespace, key_text)
        # Here we would normally use redis.get(key)
        return self._local_cache.get(key)

    async def set(self, namespace: str, key_text: str, value: Any, ttl_seconds: int = 86400):
        """Set value in cache with a TTL (default 24h)."""
        key = self._generate_key(namespace, key_text)
        # Here we would normally use redis.setex(key, ttl_seconds, json.dumps(value))
        self._local_cache[key] = value
        logger.debug(f"Cached key: {key} for namespace: {namespace}")

_cache_service_instance = None

def get_cache_service_instance() -> CacheService:
    global _cache_service_instance
    if _cache_service_instance is None:
        _cache_service_instance = CacheService()
    return _cache_service_instance

