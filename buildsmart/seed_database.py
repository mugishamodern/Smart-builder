#!/usr/bin/env python3
"""
Database seeding script for BuildSmart application.
Creates comprehensive sample data for testing and demonstration.
"""

import os
import sys
from datetime import datetime, timedelta
import random
from decimal import Decimal

from sqlalchemy import text

# Add the app directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'app'))

from app import create_app
from app.extensions import db, bcrypt
from app.models import (
    User,
    Shop,
    Product,
    Service,
    Order,
    OrderItem,
    Recommendation,
    Category,
    Cart,
    CartItem,
    Payment,
    Review
)


def clear_database():
    """Remove existing data without dropping tables (preserves migrations)."""
    print("🧹 Clearing existing data...")

    with db.engine.begin() as connection:
        # Disable FK constraints for cleanup (SQLite specific pragma is a no-op on other backends)
        connection.execute(text("PRAGMA foreign_keys = OFF"))

        for table in reversed(db.metadata.sorted_tables):
            connection.execute(table.delete())

        connection.execute(text("PRAGMA foreign_keys = ON"))

    db.session.commit()

def create_sample_data():
    """Create comprehensive sample data for the database."""
    
    print("🌱 Starting database seeding...")
    
    # Clear existing data while keeping schema intact
    clear_database()
    
    # Create users
    print("👥 Creating users...")
    users = []
    
    # Admin user
    admin_user = User(
        username='admin',
        email='admin@buildsmart.com',
        full_name='BuildSmart Administrator',
        phone='+256700000001',
        address='Kampala, Uganda',
        latitude=0.3476,
        longitude=32.5825,
        user_type='admin',
        is_active=True,
        is_verified=True,
        email_verified=True,
        email_verified_at=datetime.utcnow()
    )
    admin_user.set_password('admin123')
    users.append(admin_user)
    db.session.add(admin_user)

    # Customer users
    customer_data = [
        {
            'username': 'john_doe',
            'email': 'john@example.com',
            'full_name': 'John Doe',
            'phone': '+256700123456',
            'address': 'Kampala, Uganda',
            'latitude': 0.3476,
            'longitude': 32.5825,
            'user_type': 'customer'
        },
        {
            'username': 'mary_smith',
            'email': 'mary@example.com',
            'full_name': 'Mary Smith',
            'phone': '+256700234567',
            'address': 'Entebbe, Uganda',
            'latitude': 0.0644,
            'longitude': 32.4615,
            'user_type': 'customer'
        },
        {
            'username': 'peter_wilson',
            'email': 'peter@example.com',
            'full_name': 'Peter Wilson',
            'phone': '+256700345678',
            'address': 'Jinja, Uganda',
            'latitude': 0.4244,
            'longitude': 33.2042,
            'user_type': 'customer'
        },
        {
            'username': 'sarah_jones',
            'email': 'sarah@example.com',
            'full_name': 'Sarah Jones',
            'phone': '+256700456789',
            'address': 'Mbarara, Uganda',
            'latitude': -0.6104,
            'longitude': 30.6600,
            'user_type': 'customer'
        }
    ]
    
    for user_data in customer_data:
        user = User(**user_data)
        user.set_password('password123')
        users.append(user)
        db.session.add(user)
    
    # Shop owner users
    shop_owner_data = [
        {
            'username': 'shop_owner_1',
            'email': 'owner1@buildsmart.com',
            'full_name': 'David Kato',
            'phone': '+256700111222',
            'address': 'Ntinda, Kampala',
            'latitude': 0.3537,
            'longitude': 32.6136,
            'user_type': 'shop_owner'
        },
        {
            'username': 'shop_owner_2',
            'email': 'owner2@buildsmart.com',
            'full_name': 'Grace Nakamya',
            'phone': '+256700333444',
            'address': 'Naalya, Kampala',
            'latitude': 0.3673,
            'longitude': 32.6503,
            'user_type': 'shop_owner'
        },
        {
            'username': 'shop_owner_3',
            'email': 'owner3@buildsmart.com',
            'full_name': 'Robert Ssemwogerere',
            'phone': '+256700555666',
            'address': 'Kisugu, Kampala',
            'latitude': 0.3100,
            'longitude': 32.5800,
            'user_type': 'shop_owner'
        }
    ]
    
    for user_data in shop_owner_data:
        user = User(**user_data)
        user.set_password('password123')
        users.append(user)
        db.session.add(user)
    
    # Service provider users
    service_provider_data = [
        {
            'username': 'contractor_mike',
            'email': 'mike@contractors.com',
            'full_name': 'Michael Ochieng',
            'phone': '+256700777888',
            'address': 'Kololo, Kampala',
            'latitude': 0.3333,
            'longitude': 32.6167,
            'user_type': 'service_provider'
        },
        {
            'username': 'electrician_jane',
            'email': 'jane@electricians.com',
            'full_name': 'Jane Nakato',
            'phone': '+256700999000',
            'address': 'Bukoto, Kampala',
            'latitude': 0.3500,
            'longitude': 32.6000,
            'user_type': 'service_provider'
        }
    ]
    
    for user_data in service_provider_data:
        user = User(**user_data)
        user.set_password('password123')
        users.append(user)
        db.session.add(user)
    
    db.session.commit()
    print(f"✅ Created {len(users)} users")
    
    # Create shops
    print("🏪 Creating shops...")
    shops = []
    
    shop_data = [
        {
            'name': 'BuildMart Hardware',
            'owner_id': users[4].id,  # David Kato
            'description': 'Your one-stop shop for quality building materials and construction supplies',
            'phone': '+256700111222',
            'email': 'info@buildmart.com',
            'address': 'Ntinda, Kampala',
            'latitude': 0.3537,
            'longitude': 32.6136,
            'rating': 4.5,
            'total_reviews': 120,
            'is_verified': True
        },
        {
            'name': 'Quality Cement Supplies',
            'owner_id': users[5].id,  # Grace Nakamya
            'description': 'Wholesale and retail cement and construction materials with delivery services',
            'phone': '+256700333444',
            'email': 'sales@qualitycement.com',
            'address': 'Naalya, Kampala',
            'latitude': 0.3673,
            'longitude': 32.6503,
            'rating': 4.2,
            'total_reviews': 85,
            'is_verified': True
        },
        {
            'name': 'Steel & Steel Works',
            'owner_id': users[6].id,  # Robert Ssemwogerere
            'description': 'Specialized steel products, reinforcement bars, and metal works',
            'phone': '+256700555666',
            'email': 'steel@steelworks.com',
            'address': 'Kisugu, Kampala',
            'latitude': 0.3100,
            'longitude': 32.5800,
            'rating': 4.7,
            'total_reviews': 95,
            'is_verified': True
        },
        {
            'name': 'EcoBuild Materials',
            'owner_id': users[4].id,  # David Kato (second shop)
            'description': 'Eco-friendly building materials and sustainable construction solutions',
            'phone': '+256700111333',
            'email': 'eco@ecobuild.com',
            'address': 'Lubowa, Kampala',
            'latitude': 0.3000,
            'longitude': 32.5500,
            'rating': 4.3,
            'total_reviews': 67,
            'is_verified': True
        },
        {
            'name': 'Rooftop Supplies',
            'owner_id': users[5].id,  # Grace Nakamya (second shop)
            'description': 'Roofing materials, gutters, and weatherproofing solutions',
            'phone': '+256700333555',
            'email': 'roof@rooftop.com',
            'address': 'Kawempe, Kampala',
            'latitude': 0.3800,
            'longitude': 32.5800,
            'rating': 4.1,
            'total_reviews': 43,
            'is_verified': False
        }
    ]
    
    for shop_info in shop_data:
        shop = Shop(**shop_info)
        shops.append(shop)
        db.session.add(shop)
    
    db.session.commit()
    print(f"✅ Created {len(shops)} shops")
    
    # Create products
    print("📦 Creating products...")
    products = []
    
    # Product categories and data
    product_categories = {
        'cement': [
            {'name': 'Portland Cement 50kg', 'brand': 'Hima', 'price': 35000, 'unit': 'bags'},
            {'name': 'Tororo Cement 50kg', 'brand': 'Tororo', 'price': 34000, 'unit': 'bags'},
            {'name': 'Lafarge Cement 50kg', 'brand': 'Lafarge', 'price': 36000, 'unit': 'bags'},
            {'name': 'Kampala Cement 50kg', 'brand': 'Kampala', 'price': 33000, 'unit': 'bags'},
        ],
        'bricks': [
            {'name': 'Red Bricks', 'brand': 'Local', 'price': 600, 'unit': 'pieces'},
            {'name': 'Interlocking Bricks', 'brand': 'Makiga', 'price': 800, 'unit': 'pieces'},
            {'name': 'Hollow Blocks', 'brand': 'Local', 'price': 1200, 'unit': 'pieces'},
            {'name': 'Solid Blocks', 'brand': 'Local', 'price': 1000, 'unit': 'pieces'},
        ],
        'steel': [
            {'name': 'Steel Bars 12mm', 'brand': 'Roofings', 'price': 4500, 'unit': 'kg'},
            {'name': 'Steel Bars 16mm', 'brand': 'Roofings', 'price': 4400, 'unit': 'kg'},
            {'name': 'Steel Bars 20mm', 'brand': 'Roofings', 'price': 4300, 'unit': 'kg'},
            {'name': 'Steel Mesh', 'brand': 'Local', 'price': 5000, 'unit': 'sqm'},
        ],
        'sand': [
            {'name': 'River Sand', 'brand': 'Local', 'price': 120000, 'unit': 'tons'},
            {'name': 'Machine Sand', 'brand': 'Local', 'price': 100000, 'unit': 'tons'},
            {'name': 'Pit Sand', 'brand': 'Local', 'price': 80000, 'unit': 'tons'},
        ],
        'aggregate': [
            {'name': 'Aggregate Stones', 'brand': 'Local', 'price': 150000, 'unit': 'tons'},
            {'name': 'Ballast', 'brand': 'Local', 'price': 130000, 'unit': 'tons'},
            {'name': 'Gravel', 'brand': 'Local', 'price': 110000, 'unit': 'tons'},
        ],
        'roofing': [
            {'name': 'Iron Sheets 28G', 'brand': 'Roofings', 'price': 42000, 'unit': 'pieces'},
            {'name': 'Iron Sheets 30G', 'brand': 'Roofings', 'price': 38000, 'unit': 'pieces'},
            {'name': 'Aluminum Sheets', 'brand': 'Aluplus', 'price': 55000, 'unit': 'pieces'},
            {'name': 'Tiles', 'brand': 'Local', 'price': 15000, 'unit': 'sqm'},
        ],
        'paint': [
            {'name': 'White Emulsion', 'brand': 'Crown', 'price': 35000, 'unit': 'liters'},
            {'name': 'Oil Paint', 'brand': 'Sadolin', 'price': 40000, 'unit': 'liters'},
            {'name': 'Primer', 'brand': 'Crown', 'price': 30000, 'unit': 'liters'},
            {'name': 'Undercoat', 'brand': 'Sadolin', 'price': 32000, 'unit': 'liters'},
        ],
        'electrical': [
            {'name': 'Cable 2.5mm', 'brand': 'Local', 'price': 3500, 'unit': 'meters'},
            {'name': 'Cable 4.0mm', 'brand': 'Local', 'price': 5500, 'unit': 'meters'},
            {'name': 'Switch', 'brand': 'Schneider', 'price': 15000, 'unit': 'pieces'},
            {'name': 'Socket', 'brand': 'Schneider', 'price': 12000, 'unit': 'pieces'},
        ],
        'plumbing': [
            {'name': 'PVC Pipes 3 inch', 'brand': 'Local', 'price': 12000, 'unit': 'meters'},
            {'name': 'PVC Pipes 4 inch', 'brand': 'Local', 'price': 15000, 'unit': 'meters'},
            {'name': 'Copper Pipes', 'brand': 'Local', 'price': 25000, 'unit': 'meters'},
            {'name': 'Fittings', 'brand': 'Local', 'price': 5000, 'unit': 'pieces'},
        ]
    }
    
    for shop in shops:
        for category, category_products in product_categories.items():
            for product_info in category_products:
                # Randomly assign some products to each shop
                if random.random() < 0.7:  # 70% chance each product appears in each shop
                    product = Product(
                        name=product_info['name'],
                        description=f"High-quality {product_info['name'].lower()} for construction projects",
                        category=category,
                        price=Decimal(str(product_info['price'])),
                        unit=product_info['unit'],
                        quantity_available=random.randint(50, 1000),
                        min_order_quantity=random.randint(1, 10),
                        brand=product_info['brand'],
                        shop_id=shop.id,
                        is_available=True
                    )
                    products.append(product)
                    db.session.add(product)
    
    db.session.commit()
    print(f"✅ Created {len(products)} products")
    
    # Create services
    print("🔧 Creating services...")
    services = []
    
    service_data = [
        {
            'title': 'General Construction',
            'description': 'Complete construction services for residential and commercial buildings',
            'service_type': 'construction',
            'hourly_rate': Decimal('15000'),
            'years_experience': 8,
            'rating': 4.6,
            'service_area': 'Kampala, Entebbe',
            'certifications': 'Uganda National Association of Building and Civil Engineering Contractors',
            'provider_id': users[7].id  # Michael Ochieng
        },
        {
            'title': 'Electrical Installation',
            'description': 'Professional electrical wiring, installation, and maintenance services',
            'service_type': 'electrical',
            'hourly_rate': Decimal('12000'),
            'years_experience': 6,
            'rating': 4.8,
            'service_area': 'Kampala, Wakiso',
            'certifications': 'Uganda Institution of Professional Engineers',
            'provider_id': users[8].id  # Jane Nakato
        },
        {
            'title': 'Plumbing Services',
            'description': 'Complete plumbing installation, repair, and maintenance',
            'service_type': 'plumbing',
            'hourly_rate': Decimal('10000'),
            'years_experience': 5,
            'rating': 4.4,
            'service_area': 'Kampala',
            'certifications': 'Uganda Plumbers Association',
            'provider_id': users[7].id  # Michael Ochieng
        },
        {
            'title': 'Roofing Installation',
            'description': 'Professional roofing installation and repair services',
            'service_type': 'roofing',
            'hourly_rate': Decimal('18000'),
            'years_experience': 10,
            'rating': 4.7,
            'service_area': 'Kampala, Mukono',
            'certifications': 'Uganda Roofing Contractors Association',
            'provider_id': users[8].id  # Jane Nakato
        }
    ]
    
    for service_info in service_data:
        service = Service(**service_info)
        services.append(service)
        db.session.add(service)
    
    db.session.commit()
    print(f"✅ Created {len(services)} services")
    
    # Create orders
    print("📋 Creating orders...")
    orders = []
    
    # Generate orders for the last 3 months
    for i in range(50):  # Create 50 orders
        customer = random.choice([u for u in users if u.user_type == 'customer'])
        shop = random.choice(shops)
        shop_products = [p for p in products if p.shop_id == shop.id]
        
        if not shop_products:
            continue
            
        # Create order
        order = Order(
            order_number=f"ORD{datetime.now().strftime('%Y%m%d')}{i+1:03d}",
            status=random.choice(['pending', 'confirmed', 'processing', 'shipped', 'delivered']),
            total_amount=Decimal('0'),
            subtotal_amount=Decimal('0'),
            discount_amount=Decimal('0'),
            tax_amount=Decimal('0'),
            delivery_address=customer.address,
            delivery_notes=f"Order notes for order {i+1}",
            payment_status=random.choice(['pending', 'paid', 'failed']),
            payment_method=random.choice(['cash', 'mobile_money', 'bank_transfer']),
            coupon_code=None,
            customer_id=customer.id,
            shop_id=shop.id,
            created_at=datetime.now() - timedelta(days=random.randint(1, 90))
        )
        
        db.session.add(order)
        db.session.flush()  # Flush to get the order ID
        
        # Create order items
        num_items = random.randint(1, 5)
        selected_products = random.sample(shop_products, min(num_items, len(shop_products)))
        
        total_amount = Decimal('0')
        for product in selected_products:
            quantity = random.randint(1, 10)
            unit_price = product.price
            total_price = unit_price * quantity
            
            order_item = OrderItem(
                quantity=quantity,
                unit_price=unit_price,
                total_price=total_price,
                order_id=order.id,
                product_id=product.id
            )
            
            total_amount += total_price
            db.session.add(order_item)
        
        order.subtotal_amount = total_amount
        order.discount_amount = Decimal('0')
        order.tax_amount = (total_amount * Decimal('0.05')).quantize(Decimal('0.01'))
        order.total_amount = order.subtotal_amount - order.discount_amount + order.tax_amount
        orders.append(order)
    
    db.session.commit()
    print(f"✅ Created {len(orders)} orders")
    
    # Create recommendations
    print("🤖 Creating recommendations...")
    recommendations = []
    
    recommendation_templates = [
        {
            'project_type': '2_bedroom_house',
            'project_description': 'Modern 2-bedroom house with open plan living, kitchen, and bathroom. Includes foundation, walls, roofing, and basic finishes.',
            'total_estimated_cost': Decimal('45000000')
        },
        {
            'project_type': '3_bedroom_house',
            'project_description': 'Spacious 3-bedroom family home with master bedroom ensuite, living room, dining area, and modern kitchen.',
            'total_estimated_cost': Decimal('65000000')
        },
        {
            'project_type': 'office_building',
            'project_description': 'Small office building with 4 rooms, reception area, and parking space. Suitable for small business operations.',
            'total_estimated_cost': Decimal('85000000')
        },
        {
            'project_type': 'renovation',
            'project_description': 'Complete home renovation including kitchen upgrade, bathroom remodeling, and interior painting.',
            'total_estimated_cost': Decimal('15000000')
        },
        {
            'project_type': 'extension',
            'project_description': 'House extension adding 2 additional bedrooms and a family room to existing structure.',
            'total_estimated_cost': Decimal('25000000')
        }
    ]
    
    for customer in [u for u in users if u.user_type == 'customer']:
        # Create 2-5 recommendations per customer
        num_recs = random.randint(2, 5)
        for i in range(num_recs):
            template = random.choice(recommendation_templates)
            
            recommendation = Recommendation(
                project_type=template['project_type'],
                project_description=template['project_description'],
                total_estimated_cost=template['total_estimated_cost'],
                recommendation_data={
                    'materials': [
                        {'name': 'Cement', 'quantity': random.randint(50, 100), 'unit': 'bags'},
                        {'name': 'Bricks', 'quantity': random.randint(2000, 5000), 'unit': 'pieces'},
                        {'name': 'Steel Bars', 'quantity': random.randint(500, 1000), 'unit': 'kg'},
                        {'name': 'Sand', 'quantity': random.randint(10, 20), 'unit': 'tons'},
                    ],
                    'estimated_duration': f"{random.randint(3, 12)} months",
                    'complexity': random.choice(['Low', 'Medium', 'High']),
                    'confidence_score': round(random.uniform(0.7, 0.95), 2)
                },
                is_saved=random.choice([True, False]),
                user_id=customer.id,
                created_at=datetime.now() - timedelta(days=random.randint(1, 30))
            )
            
            recommendations.append(recommendation)
            db.session.add(recommendation)
    
    db.session.commit()
    print(f"✅ Created {len(recommendations)} recommendations")
    
    print("\n🎉 Database seeding completed successfully!")
    print("\n📊 Summary:")
    print(f"   👥 Users: {len(users)}")
    print(f"   🏪 Shops: {len(shops)}")
    print(f"   📦 Products: {len(products)}")
    print(f"   🔧 Services: {len(services)}")
    print(f"   📋 Orders: {len(orders)}")
    print(f"   🤖 Recommendations: {len(recommendations)}")
    
    print("\n🔑 Test Credentials:")
    print("   Customer: john_doe / password123")
    print("   Shop Owner: shop_owner_1 / password123")
    print("   Service Provider: contractor_mike / password123")

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        create_sample_data()
