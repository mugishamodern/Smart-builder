"""
Database index utilities and recommendations.

This module provides utilities for creating and managing database indexes
for optimal query performance.
"""
from app.extensions import db
from sqlalchemy import Index


# Recommended indexes for common queries
RECOMMENDED_INDEXES = {
    'users': [
        ('email',),
        ('username',),
        ('user_type',),
        ('created_at',),
    ],
    'shops': [
        ('owner_id',),
        ('is_verified',),
        ('is_active',),
        ('created_at',),
        ('latitude', 'longitude'),  # Composite index for location queries
    ],
    'products': [
        ('shop_id',),
        ('category_id',),
        ('is_available',),
        ('price',),
        ('created_at',),
        ('shop_id', 'category_id'),  # Composite index
        ('shop_id', 'is_available'),  # Composite index
    ],
    'orders': [
        ('customer_id',),
        ('shop_id',),
        ('status',),
        ('payment_status',),
        ('created_at',),
        ('customer_id', 'status'),  # Composite index
        ('shop_id', 'status'),  # Composite index
    ],
    'order_items': [
        ('order_id',),
        ('product_id',),
    ],
    'reviews': [
        ('shop_id',),
        ('product_id',),
        ('user_id',),
        ('is_approved',),
        ('rating',),
    ],
    'messages': [
        ('conversation_id',),
        ('sender_id',),
        ('is_read',),
        ('created_at',),
    ],
    'notifications': [
        ('user_id',),
        ('is_read',),
        ('created_at',),
        ('user_id', 'is_read'),  # Composite index
    ],
    'wallets': [
        ('user_id',),
    ],
    'transactions': [
        ('wallet_id',),
        ('transaction_type',),
        ('status',),
        ('created_at',),
    ],
    'analytics_metrics': [
        ('metric_type',),
        ('metric_date',),
        ('shop_id',),
        ('category_id',),
        ('user_id',),
    ],
}


def create_recommended_indexes():
    """
    Create recommended database indexes.
    
    This function should be run as a migration or during database setup.
    Note: This is a helper function - actual indexes should be created via migrations.
    """
    # This is a reference implementation
    # Actual indexes should be created via Alembic migrations
    
    indexes_created = []
    
    for table_name, index_defs in RECOMMENDED_INDEXES.items():
        for index_def in index_defs:
            index_name = f"idx_{table_name}_{'_'.join(index_def)}"
            # In a real migration, you would create the index here
            indexes_created.append((table_name, index_name, index_def))
    
    return indexes_created


def get_table_indexes(table_name: str) -> List[tuple]:
    """
    Get recommended indexes for a table.
    
    Args:
        table_name: Name of the table
    
    Returns:
        List of index definitions (columns)
    """
    return RECOMMENDED_INDEXES.get(table_name, [])


def should_create_index(table_name: str, columns: tuple) -> bool:
    """
    Check if an index should be created for given columns.
    
    Args:
        table_name: Name of the table
        columns: Column names tuple
    
    Returns:
        True if index should be created
    """
    recommended = RECOMMENDED_INDEXES.get(table_name, [])
    return columns in recommended or tuple(reversed(columns)) in recommended

