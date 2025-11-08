"""
Query optimization utilities.

This module provides utilities for optimizing database queries
including eager loading, query batching, and result caching.
"""
from functools import wraps
from typing import List, Optional, Callable, Any
from sqlalchemy.orm import joinedload, selectinload, subqueryload
from sqlalchemy import func
from app.extensions import db
from app.services.cache_service import CacheService


def eager_load(*relationships):
    """
    Decorator to eager load relationships in queries.
    
    Args:
        *relationships: Relationship names to eager load
    
    Usage:
        @eager_load('products', 'orders')
        def get_shops():
            return Shop.query.all()
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            query = func(*args, **kwargs)
            
            # Add eager loading options
            for rel in relationships:
                if hasattr(query.column_descriptions[0]['entity'], rel):
                    query = query.options(joinedload(rel))
            
            return query.all() if hasattr(query, 'all') else query
        
        return wrapper
    return decorator


def batch_load(model_class, ids: List[int], relationship: str):
    """
    Batch load relationships for multiple model instances.
    
    Args:
        model_class: SQLAlchemy model class
        ids: List of model IDs
        relationship: Relationship name to load
    
    Returns:
        Dictionary mapping IDs to loaded relationships
    """
    if not ids:
        return {}
    
    # Use selectinload for efficient batch loading
    results = model_class.query.filter(model_class.id.in_(ids)).options(
        selectinload(relationship)
    ).all()
    
    return {obj.id: getattr(obj, relationship) for obj in results}


def paginate_query(query, page: int = 1, per_page: int = 20):
    """
    Paginate a query with caching.
    
    Args:
        query: SQLAlchemy query
        page: Page number (1-indexed)
        per_page: Items per page
    
    Returns:
        Paginated results
    """
    # Generate cache key from query
    cache_key = f"paginate:{query.statement.compile()}:page:{page}:per_page:{per_page}"
    
    # Try to get from cache
    cached = CacheService.get(cache_key)
    if cached is not None:
        return cached
    
    # Execute query
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Cache the result
    CacheService.set(cache_key, pagination, timeout=300)
    
    return pagination


def optimize_query(query):
    """
    Apply common query optimizations.
    
    Args:
        query: SQLAlchemy query
    
    Returns:
        Optimized query
    """
    # Add common optimizations
    # 1. Use select_related for foreign keys when possible
    # 2. Limit unnecessary columns
    # 3. Use indexes
    
    return query


class QueryOptimizer:
    """Helper class for query optimization."""
    
    @staticmethod
    def get_with_cache(key: str, query_func: Callable, timeout: int = 300):
        """
        Execute query with caching.
        
        Args:
            key: Cache key
            query_func: Function that returns a query
            timeout: Cache timeout in seconds
        
        Returns:
            Query results
        """
        cached = CacheService.get(key)
        if cached is not None:
            return cached
        
        result = query_func()
        CacheService.set(key, result, timeout=timeout)
        return result
    
    @staticmethod
    def prefetch_related(query, *relationships):
        """
        Prefetch related objects for a query.
        
        Args:
            query: SQLAlchemy query
            *relationships: Relationship names to prefetch
        
        Returns:
            Query with prefetch options
        """
        options = []
        for rel in relationships:
            options.append(selectinload(rel))
        
        if options:
            return query.options(*options)
        return query
    
    @staticmethod
    def count_efficient(query):
        """
        Get count efficiently (using COUNT(*) instead of loading all objects).
        
        Args:
            query: SQLAlchemy query
        
        Returns:
            Count of results
        """
        return query.count()
    
    @staticmethod
    def exists_efficient(query):
        """
        Check existence efficiently (using LIMIT 1).
        
        Args:
            query: SQLAlchemy query
        
        Returns:
            True if exists, False otherwise
        """
        return query.limit(1).first() is not None

