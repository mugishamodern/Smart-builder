"""
Response caching middleware.

This module provides middleware for caching HTTP responses
to improve performance for frequently accessed endpoints.
"""
from functools import wraps
from typing import Optional, Callable
from flask import request, make_response, has_request_context
from app.services.cache_service import CacheService


def cache_response(timeout: int = 300, key_prefix: str = 'response', 
                  vary_on: Optional[list] = None, 
                  condition: Optional[Callable] = None):
    """
    Decorator to cache HTTP responses.
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
        key_prefix: Cache key prefix
        vary_on: List of headers/params to vary cache on (e.g., ['Authorization'])
        condition: Optional function to determine if response should be cached
    
    Usage:
        @cache_response(timeout=600, vary_on=['Authorization'])
        def my_view():
            return jsonify({'data': 'value'})
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not has_request_context():
                return func(*args, **kwargs)
            
            # Generate cache key
            cache_key_parts = [key_prefix, request.method, request.path]
            
            # Add query parameters
            if request.args:
                sorted_args = sorted(request.args.items())
                cache_key_parts.append('&'.join([f"{k}={v}" for k, v in sorted_args]))
            
            # Add vary_on headers/params
            if vary_on:
                for item in vary_on:
                    value = request.headers.get(item) or request.args.get(item)
                    if value:
                        cache_key_parts.append(f"{item}:{value}")
            
            cache_key = ':'.join(cache_key_parts)
            
            # Check cache
            cached_response = CacheService.get(cache_key)
            if cached_response is not None:
                # Recreate response from cached data
                response = make_response(cached_response['data'])
                for header, value in cached_response.get('headers', {}).items():
                    response.headers[header] = value
                response.status_code = cached_response.get('status_code', 200)
                return response
            
            # Execute function
            result = func(*args, **kwargs)
            
            # Check if we should cache this response
            if condition and not condition(result):
                return result
            
            # Cache the response
            response_data = {
                'data': result.data if hasattr(result, 'data') else str(result),
                'status_code': result.status_code if hasattr(result, 'status_code') else 200,
                'headers': dict(result.headers) if hasattr(result, 'headers') else {}
            }
            
            CacheService.set(cache_key, response_data, timeout=timeout)
            
            return result
        
        return wrapper
    return decorator


def cache_public(timeout: int = 3600):
    """
    Cache decorator for public endpoints (no authentication required).
    
    Args:
        timeout: Cache timeout in seconds (default: 1 hour)
    
    Usage:
        @cache_public(timeout=7200)
        def public_api():
            return jsonify({'data': 'value'})
    """
    return cache_response(timeout=timeout, key_prefix='public', vary_on=None)


def cache_private(timeout: int = 300):
    """
    Cache decorator for private endpoints (requires authentication).
    
    Args:
        timeout: Cache timeout in seconds (default: 5 minutes)
    
    Usage:
        @cache_private(timeout=600)
        @login_required
        def private_api():
            return jsonify({'data': 'value'})
    """
    return cache_response(timeout=timeout, key_prefix='private', 
                         vary_on=['Authorization'])


def no_cache():
    """
    Decorator to ensure response is not cached.
    
    Usage:
        @no_cache()
        def sensitive_data():
            return jsonify({'data': 'value'})
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            if hasattr(result, 'headers'):
                result.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
                result.headers['Pragma'] = 'no-cache'
                result.headers['Expires'] = '0'
            return result
        return wrapper
    return decorator

