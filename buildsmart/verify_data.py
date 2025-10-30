#!/usr/bin/env python3
"""
Script to verify the seeded data in the database.
"""

import os
import sys

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.extensions import db
from app.models import User, Shop, Product, Service, Order, OrderItem, Recommendation

def verify_data():
    """Verify the seeded data in the database."""
    
    app = create_app()
    with app.app_context():
        print("🔍 Verifying seeded data...")
        
        # Count records
        user_count = User.query.count()
        shop_count = Shop.query.count()
        product_count = Product.query.count()
        service_count = Service.query.count()
        order_count = Order.query.count()
        order_item_count = OrderItem.query.count()
        recommendation_count = Recommendation.query.count()
        
        print(f"\n📊 Database Statistics:")
        print(f"   👥 Users: {user_count}")
        print(f"   🏪 Shops: {shop_count}")
        print(f"   📦 Products: {product_count}")
        print(f"   🔧 Services: {service_count}")
        print(f"   📋 Orders: {order_count}")
        print(f"   📋 Order Items: {order_item_count}")
        print(f"   🤖 Recommendations: {recommendation_count}")
        
        # Show some sample data
        print(f"\n👥 Sample Users:")
        for user in User.query.limit(3):
            print(f"   - {user.username} ({user.user_type}) - {user.full_name}")
        
        print(f"\n🏪 Sample Shops:")
        for shop in Shop.query.limit(3):
            print(f"   - {shop.name} - {shop.address}")
        
        print(f"\n📦 Sample Products:")
        for product in Product.query.limit(5):
            print(f"   - {product.name} ({product.category}) - UGX {product.price:,}")
        
        print(f"\n🔧 Sample Services:")
        for service in Service.query.limit(3):
            print(f"   - {service.title} ({service.service_type}) - UGX {service.hourly_rate:,}/hr")
        
        print(f"\n📋 Sample Orders:")
        for order in Order.query.limit(3):
            print(f"   - {order.order_number} - UGX {order.total_amount:,} ({order.status})")
        
        print(f"\n🤖 Sample Recommendations:")
        for rec in Recommendation.query.limit(3):
            print(f"   - {rec.project_type} - UGX {rec.total_estimated_cost:,}")
        
        print(f"\n✅ Data verification completed!")

if __name__ == '__main__':
    verify_data()
