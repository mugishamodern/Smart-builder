"""
Tests for product comparison feature.
"""
import pytest
from app.extensions import db
from app.models import User, Shop, Product, Comparison
from app.extensions import bcrypt


def test_add_to_comparison(db, auth_client):
    """Test adding a product to comparison."""
    client, user = auth_client
    
    # Create a shop and product
    shop = Shop(
        name='Test Shop',
        address='Test Address',
        latitude=0.0,
        longitude=0.0,
        owner_id=user.id
    )
    db.session.add(shop)
    db.session.commit()
    
    product = Product(
        shop_id=shop.id,
        name='Test Product',
        category='cement',
        price=10000,
        quantity_available=100,
        unit='bags'
    )
    db.session.add(product)
    db.session.commit()
    
    # Add to comparison via API
    response = client.post('/api/comparisons/add', json={
        'product_id': product.id
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify comparison in database
    comparison = Comparison.query.filter_by(
        user_id=user.id,
        product_id=product.id
    ).first()
    assert comparison is not None


def test_get_comparisons(db, auth_client):
    """Test getting user's comparisons."""
    client, user = auth_client
    
    # Create shop and products
    shop = Shop(
        name='Test Shop',
        address='Test Address',
        latitude=0.0,
        longitude=0.0,
        owner_id=user.id
    )
    db.session.add(shop)
    db.session.commit()
    
    product1 = Product(
        shop_id=shop.id,
        name='Product 1',
        category='cement',
        price=10000,
        quantity_available=100,
        unit='bags'
    )
    product2 = Product(
        shop_id=shop.id,
        name='Product 2',
        category='cement',
        price=12000,
        quantity_available=100,
        unit='bags'
    )
    db.session.add_all([product1, product2])
    db.session.commit()
    
    # Create comparisons
    comp1 = Comparison(user_id=user.id, product_id=product1.id)
    comp2 = Comparison(user_id=user.id, product_id=product2.id)
    db.session.add_all([comp1, comp2])
    db.session.commit()
    
    # Get comparisons via API
    response = client.get('/api/comparisons')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['products']) == 2


def test_remove_from_comparison(db, auth_client):
    """Test removing a product from comparison."""
    client, user = auth_client
    
    # Create shop and product
    shop = Shop(
        name='Test Shop',
        address='Test Address',
        latitude=0.0,
        longitude=0.0,
        owner_id=user.id
    )
    db.session.add(shop)
    db.session.commit()
    
    product = Product(
        shop_id=shop.id,
        name='Test Product',
        category='cement',
        price=10000,
        quantity_available=100,
        unit='bags'
    )
    db.session.add(product)
    db.session.commit()
    
    # Add to comparison
    comparison = Comparison(user_id=user.id, product_id=product.id)
    db.session.add(comparison)
    db.session.commit()
    
    # Remove from comparison via API
    response = client.delete(f'/api/comparisons/{product.id}/remove')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify comparison is removed
    comparison = Comparison.query.filter_by(
        user_id=user.id,
        product_id=product.id
    ).first()
    assert comparison is None


def test_clear_comparisons(db, auth_client):
    """Test clearing all comparisons."""
    client, user = auth_client
    
    # Create shop and products
    shop = Shop(
        name='Test Shop',
        address='Test Address',
        latitude=0.0,
        longitude=0.0,
        owner_id=user.id
    )
    db.session.add(shop)
    db.session.commit()
    
    product1 = Product(
        shop_id=shop.id,
        name='Product 1',
        category='cement',
        price=10000,
        quantity_available=100,
        unit='bags'
    )
    product2 = Product(
        shop_id=shop.id,
        name='Product 2',
        category='cement',
        price=12000,
        quantity_available=100,
        unit='bags'
    )
    db.session.add_all([product1, product2])
    db.session.commit()
    
    # Create comparisons
    comp1 = Comparison(user_id=user.id, product_id=product1.id)
    comp2 = Comparison(user_id=user.id, product_id=product2.id)
    db.session.add_all([comp1, comp2])
    db.session.commit()
    
    # Clear comparisons via API
    response = client.delete('/api/comparisons/clear')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify all comparisons are removed
    comparisons = Comparison.query.filter_by(user_id=user.id).all()
    assert len(comparisons) == 0
