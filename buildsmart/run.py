import os
from app import create_app
from app.extensions import db
from app.models import User, Shop, Product, Service

app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell"""
    return {
        'db': db,
        'User': User,
        'Shop': Shop,
        'Product': Product,
        'Service': Service
    }


@app.cli.command()
def init_db():
    """Initialize the database with sample data"""
    from app.extensions import bcrypt
    
    db.create_all()
    
    # Create sample users
    if not User.query.first():
        # Customer user
        customer = User(
            username='john_doe',
            email='john@example.com',
            password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
            full_name='John Doe',
            phone='+256700123456',
            address='Kampala, Uganda',
            latitude=0.3476,
            longitude=32.5825,
            user_type='customer'
        )
        
        # Shop owner user
        shop_owner = User(
            username='shop_owner',
            email='owner@buildsmart.com',
            password_hash=bcrypt.generate_password_hash('password123').decode('utf-8'),
            full_name='Shop Owner',
            phone='+256700654321',
            user_type='customer'
        )
        
        db.session.add_all([customer, shop_owner])
        db.session.commit()
        
        # Create sample shops
        shop1 = Shop(
            name='BuildMart Hardware',
            owner_id=shop_owner.id,
            description='Your one-stop shop for quality building materials',
            phone='+256700111222',
            email='info@buildmart.com',
            address='Ntinda, Kampala',
            latitude=0.3537,
            longitude=32.6136,
            rating=4.5,
            total_reviews=120,
            is_verified=True
        )
        
        shop2 = Shop(
            name='Quality Cement Supplies',
            owner_id=shop_owner.id,
            description='Wholesale and retail cement and construction materials',
            phone='+256700333444',
            email='sales@qualitycement.com',
            address='Naalya, Kampala',
            latitude=0.3673,
            longitude=32.6503,
            rating=4.2,
            total_reviews=85,
            is_verified=True
        )
        
        db.session.add_all([shop1, shop2])
        db.session.commit()
        
        # Create sample products
        products = [
            # Shop 1 products
            Product(shop_id=shop1.id, name='Portland Cement 50kg', category='cement', 
                   unit='bags', price=35000, quantity_available=500, brand='Hima',
                   description='High-quality Portland cement for all construction needs'),
            Product(shop_id=shop1.id, name='Red Bricks', category='bricks',
                   unit='pieces', price=600, quantity_available=10000,
                   description='Durable red clay bricks'),
            Product(shop_id=shop1.id, name='Steel Bars 12mm', category='steel',
                   unit='kg', price=4500, quantity_available=2000, brand='Roofings',
                   description='High-tensile steel reinforcement bars'),
            Product(shop_id=shop1.id, name='River Sand', category='sand',
                   unit='tons', price=120000, quantity_available=50,
                   description='Clean river sand for construction'),
            Product(shop_id=shop1.id, name='Aggregate Stones', category='aggregate',
                   unit='tons', price=150000, quantity_available=30,
                   description='Crushed aggregate stones'),
            
            # Shop 2 products
            Product(shop_id=shop2.id, name='Tororo Cement 50kg', category='cement',
                   unit='bags', price=34000, quantity_available=800, brand='Tororo',
                   description='Premium quality cement from Tororo'),
            Product(shop_id=shop2.id, name='Roofing Iron Sheets', category='roofing',
                   unit='pieces', price=42000, quantity_available=200, brand='Roofings',
                   description='28-gauge iron roofing sheets'),
            Product(shop_id=shop2.id, name='Paint - White Emulsion', category='paint',
                   unit='liters', price=35000, quantity_available=100, brand='Crown',
                   description='Premium white emulsion paint'),
            Product(shop_id=shop2.id, name='Electrical Cable 2.5mm', category='electrical',
                   unit='meters', price=3500, quantity_available=500,
                   description='Quality electrical cables'),
            Product(shop_id=shop2.id, name='PVC Pipes 3 inch', category='plumbing',
                   unit='meters', price=12000, quantity_available=150,
                   description='Durable PVC plumbing pipes'),
        ]
        
        db.session.add_all(products)
        db.session.commit()
        
        print('Database initialized with sample data!')
        print('Login credentials:')
        print('Customer - Username: john_doe, Password: password123')
        print('Shop Owner - Username: shop_owner, Password: password123')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)