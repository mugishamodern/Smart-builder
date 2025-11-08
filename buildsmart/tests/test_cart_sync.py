"""
Tests for cart synchronization and saved cart features.
"""
import pytest
from app.extensions import db
from app.models import User, Shop, Product, Cart, CartItem
from app.extensions import bcrypt
from app.utils.cart_utils import merge_guest_cart_to_user


def test_merge_guest_cart(db):
    """Test merging guest cart to user cart."""
    # Create a user
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash=bcrypt.generate_password_hash('testpass123').decode('utf-8'),
        full_name='Test User',
        user_type='customer'
    )
    db.session.add(user)
    db.session.commit()
    
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
    
    # Create guest cart
    guest_cart = Cart(session_id='guest_session_123')
    db.session.add(guest_cart)
    db.session.commit()
    
    guest_item = CartItem(
        cart_id=guest_cart.id,
        product_id=product.id,
        quantity=2,
        price_snapshot=10000
    )
    db.session.add(guest_item)
    db.session.commit()
    
    # Merge guest cart to user
    merge_guest_cart_to_user('guest_session_123', user.id)
    
    # Verify user has a cart with the item
    user_cart = Cart.query.filter_by(user_id=user.id, is_saved=False).first()
    assert user_cart is not None
    
    cart_items = CartItem.query.filter_by(cart_id=user_cart.id).all()
    assert len(cart_items) == 1
    assert cart_items[0].quantity == 2
    assert cart_items[0].product_id == product.id
    
    # Verify guest cart is deleted or merged
    guest_cart = Cart.query.filter_by(session_id='guest_session_123').first()
    assert guest_cart is None or guest_cart.user_id == user.id


def test_save_cart(db, auth_client):
    """Test saving a cart for later."""
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
    
    # Create a cart with items
    cart = Cart(user_id=user.id, is_saved=False)
    db.session.add(cart)
    db.session.commit()
    
    cart_item = CartItem(
        cart_id=cart.id,
        product_id=product.id,
        quantity=2,
        price_snapshot=10000
    )
    db.session.add(cart_item)
    db.session.commit()
    
    # Save cart via API
    response = client.post('/api/user/cart/save', json={
        'cart_id': cart.id
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify cart is saved
    db.session.refresh(cart)
    assert cart.is_saved is True


def test_get_saved_carts(db, auth_client):
    """Test getting user's saved carts."""
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
    
    # Create saved cart
    saved_cart = Cart(user_id=user.id, is_saved=True)
    db.session.add(saved_cart)
    db.session.commit()
    
    cart_item = CartItem(
        cart_id=saved_cart.id,
        product_id=product.id,
        quantity=2,
        price_snapshot=10000
    )
    db.session.add(cart_item)
    db.session.commit()
    
    # Get saved carts via API
    response = client.get('/api/user/cart/saved')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['carts']) >= 1


def test_restore_saved_cart(db, auth_client):
    """Test restoring a saved cart."""
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
    
    # Create saved cart
    saved_cart = Cart(user_id=user.id, is_saved=True)
    db.session.add(saved_cart)
    db.session.commit()
    
    cart_item = CartItem(
        cart_id=saved_cart.id,
        product_id=product.id,
        quantity=2,
        price_snapshot=10000
    )
    db.session.add(cart_item)
    db.session.commit()
    
    # Restore cart via API
    response = client.post(f'/api/user/cart/restore/{saved_cart.id}')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify cart is now active (not saved)
    db.session.refresh(saved_cart)
    assert saved_cart.is_saved is False
