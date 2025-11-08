"""
Cache service for managing application caching.

This service provides methods for caching query results,
API responses, and other frequently accessed data.
"""
from functools import wraps
from typing import Optional, Callable, Any
from datetime import timedelta
from flask import current_app, has_app_context
from app.extensions import cache


class CacheService:
    """Service for cache operations."""
    
    # Cache key prefixes
    PREFIX_SHOP = 'shop'
    PREFIX_PRODUCT = 'product'
    PREFIX_CATEGORY = 'category'
    PREFIX_USER = 'user'
    PREFIX_ORDER = 'order'
    PREFIX_SEARCH = 'search'
    PREFIX_ANALYTICS = 'analytics'
    
    @staticmethod
    def get_cache_key(prefix: str, identifier: Any, *args, **kwargs) -> str:
        """
        Generate a cache key.
        
        Args:
            prefix: Cache key prefix
            identifier: Identifier (ID, name, etc.)
            *args: Additional positional arguments
            **kwargs: Additional keyword arguments
        
        Returns:
            Formatted cache key string
        """
        key_parts = [prefix, str(identifier)]
        
        # Add args if provided
        if args:
            key_parts.extend([str(arg) for arg in args])
        
        # Add kwargs if provided
        if kwargs:
            sorted_kwargs = sorted(kwargs.items())
            key_parts.extend([f"{k}:{v}" for k, v in sorted_kwargs])
        
        return ':'.join(key_parts)
    
    @staticmethod
    def get(key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            Cached value or None
        """
        try:
            return cache.get(key)
        except Exception:
            # If cache fails, return None (graceful degradation)
            return None
    
    @staticmethod
    def set(key: str, value: Any, timeout: Optional[int] = None) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            timeout: Timeout in seconds (None = use default)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cache.set(key, value, timeout=timeout)
            return True
        except Exception:
            # If cache fails, return False (graceful degradation)
            return False
    
    @staticmethod
    def delete(key: str) -> bool:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cache.delete(key)
            return True
        except Exception:
            return False
    
    @staticmethod
    def delete_pattern(pattern: str) -> int:
        """
        Delete all keys matching a pattern.
        
        Args:
            pattern: Pattern to match (e.g., 'shop:*')
        
        Returns:
            Number of keys deleted
        """
        try:
            # Get all keys matching the pattern
            keys = cache.cache._read_client.keys(pattern)
            if keys:
                cache.cache._write_client.delete(*keys)
                return len(keys)
            return 0
        except Exception:
            return 0
    
    @staticmethod
    def clear() -> bool:
        """
        Clear all cache.
        
        Returns:
            True if successful, False otherwise
        """
        try:
            cache.clear()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_or_set(key: str, func: Callable, timeout: Optional[int] = None) -> Any:
        """
        Get value from cache or set it if not present.
        
        Args:
            key: Cache key
            func: Function to call if cache miss
            timeout: Timeout in seconds
        
        Returns:
            Cached or computed value
        """
        value = CacheService.get(key)
        if value is None:
            value = func()
            CacheService.set(key, value, timeout=timeout)
        return value
    
    @staticmethod
    def invalidate_shop(shop_id: int) -> None:
        """Invalidate all cache entries for a shop."""
        patterns = [
            f"{CacheService.PREFIX_SHOP}:{shop_id}",
            f"{CacheService.PREFIX_SHOP}:{shop_id}:*",
            f"{CacheService.PREFIX_PRODUCT}:*:shop:{shop_id}",
            f"{CacheService.PREFIX_SEARCH}:*:shop:{shop_id}",
            f"{CacheService.PREFIX_ANALYTICS}:shop:{shop_id}*"
        ]
        for pattern in patterns:
            CacheService.delete_pattern(pattern)
    
    @staticmethod
    def invalidate_product(product_id: int) -> None:
        """Invalidate all cache entries for a product."""
        patterns = [
            f"{CacheService.PREFIX_PRODUCT}:{product_id}",
            f"{CacheService.PREFIX_PRODUCT}:{product_id}:*",
            f"{CacheService.PREFIX_SEARCH}:*:product:{product_id}",
            f"{CacheService.PREFIX_CATEGORY}:*:product:{product_id}"
        ]
        for pattern in patterns:
            CacheService.delete_pattern(pattern)
    
    @staticmethod
    def invalidate_user(user_id: int) -> None:
        """Invalidate all cache entries for a user."""
        patterns = [
            f"{CacheService.PREFIX_USER}:{user_id}",
            f"{CacheService.PREFIX_USER}:{user_id}:*",
            f"{CacheService.PREFIX_ORDER}:*:user:{user_id}"
        ]
        for pattern in patterns:
            CacheService.delete_pattern(pattern)
    
    @staticmethod
    def invalidate_category(category_id: int) -> None:
        """Invalidate all cache entries for a category."""
        patterns = [
            f"{CacheService.PREFIX_CATEGORY}:{category_id}",
            f"{CacheService.PREFIX_CATEGORY}:{category_id}:*",
            f"{CacheService.PREFIX_PRODUCT}:*:category:{category_id}",
            f"{CacheService.PREFIX_SEARCH}:*:category:{category_id}"
        ]
        for pattern in patterns:
            CacheService.delete_pattern(pattern)
    
    @staticmethod
    def invalidate_search() -> None:
        """Invalidate all search cache entries."""
        CacheService.delete_pattern(f"{CacheService.PREFIX_SEARCH}:*")
    
    @staticmethod
    def invalidate_analytics() -> None:
        """Invalidate all analytics cache entries."""
        CacheService.delete_pattern(f"{CacheService.PREFIX_ANALYTICS}:*")


def cached(timeout: int = 300, key_prefix: str = 'view'):
    """
    Decorator to cache view function results.
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        key_prefix: Cache key prefix
    
    Usage:
        @cached(timeout=600)
        def my_view():
            return render_template('index.html')
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            cache_key = CacheService.get_cache_key(key_prefix, func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = CacheService.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache the result
            CacheService.set(cache_key, result, timeout=timeout)
            
            return result
        
        return wrapper
    return decorator


def cached_query(timeout: int = 300, key_func: Optional[Callable] = None):
    """
    Decorator to cache database query results.
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        key_func: Optional function to generate cache key from arguments
    
    Usage:
        @cached_query(timeout=600)
        def get_products():
            return Product.query.all()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                cache_key = CacheService.get_cache_key('query', func.__name__, *args, **kwargs)
            
            # Try to get from cache
            cached_value = CacheService.get(cache_key)
            if cached_value is not None:
                return cached_value
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Cache the result
            CacheService.set(cache_key, result, timeout=timeout)
            
            return result
        
        return wrapper
    return decorator

