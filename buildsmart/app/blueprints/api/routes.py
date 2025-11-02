from flask import jsonify, request
from flask_login import login_required, current_user, login_user
from app.models import Shop, Product, Service, User, Order, Recommendation, Cart, CartItem
from app.extensions import db
from app.ai.recommender import generate_full_recommendation
from app.blueprints.api import api_bp
from app.utils.error_handlers import (
    handle_api_error, handle_validation_error, handle_permission_error,
    handle_not_found_error, validate_required_fields, validate_json_request
)
from decimal import Decimal


@api_bp.route('/shops/nearby', methods=['GET'])
def nearby_shops():
    """Get shops near a location"""
    try:
        lat = request.args.get('lat', type=float)
        lon = request.args.get('lon', type=float)
        radius = request.args.get('radius', 10, type=float)  # km
        
        if not lat or not lon:
            return handle_validation_error({'lat': 'Latitude is required', 'lon': 'Longitude is required'})
        
        # Get all verified shops
        shops = Shop.query.filter_by(is_verified=True).all()
        
        # Filter by distance
        nearby = []
        for shop in shops:
            distance = shop.distance_to(lat, lon)
            if distance <= radius:
                nearby.append({
            'id': shop.id or 0,
            'name': shop.name or '',
            'description': shop.description or '',
            'address': shop.address or '',
            'phone': shop.phone,
            'email': shop.email,
            'latitude': float(shop.latitude) if shop.latitude else 0.0,
            'longitude': float(shop.longitude) if shop.longitude else 0.0,
            'rating': float(shop.rating) if shop.rating else 0.0,
            'total_reviews': shop.total_reviews or 0,
            'is_verified': shop.is_verified if shop.is_verified is not None else False,
            'is_active': shop.is_active if shop.is_active is not None else True,
            'owner_id': shop.owner_id or 0,
            'distance_km': round(distance, 2),
        })
    
        # Sort by distance
        nearby.sort(key=lambda x: x['distance_km'])
        
        return jsonify({
            'shops': nearby,
            'count': len(nearby)
        })
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/shops/search', methods=['GET'])
def search_shops():
    """Search shops by name or description"""
    query = request.args.get('q', '')
    limit = request.args.get('limit', 20, type=int)
    
    # Build query
    shops_query = Shop.query.filter_by(is_active=True)
    
    if query:
        shops_query = shops_query.filter(
            (Shop.name.ilike(f'%{query}%')) | 
            (Shop.description.ilike(f'%{query}%'))
        )
    
    # Limit results
    shops = shops_query.limit(limit).all()
    
    shops_data = [{
        'id': s.id or 0,
        'name': s.name or '',
        'description': s.description or '',
        'address': s.address or '',
        'phone': s.phone,
        'email': s.email,
        'latitude': float(s.latitude) if s.latitude else 0.0,
        'longitude': float(s.longitude) if s.longitude else 0.0,
        'rating': float(s.rating) if s.rating else 0.0,
        'total_reviews': s.total_reviews or 0,
        'is_verified': s.is_verified if s.is_verified is not None else False,
        'is_active': s.is_active if s.is_active is not None else True,
        'owner_id': s.owner_id or 0,
        'created_at': s.created_at.isoformat() if s.created_at else None,
        'updated_at': s.updated_at.isoformat() if s.updated_at else None,
    } for s in shops]
    
    return jsonify({
        'shops': shops_data,
        'count': len(shops_data)
    }), 200


@api_bp.route('/products/search', methods=['GET'])
def search_products():
    """Search products by category or name"""
    query = request.args.get('q', '')
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    products_query = Product.query.filter_by(is_available=True)
    
    if query:
        products_query = products_query.filter(
            (Product.name.ilike(f'%{query}%')) | 
            (Product.description.ilike(f'%{query}%'))
        )
    
    if category:
        products_query = products_query.filter(Product.category == category)
    
    if min_price:
        products_query = products_query.filter(Product.price >= min_price)
    
    if max_price:
        products_query = products_query.filter(Product.price <= max_price)
    
    # Paginate
    pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    
    products = [{
        'id': p.id or 0,
        'name': p.name or '',
        'category': p.category or '',
        'price': float(p.price) if p.price else 0.0,
        'unit': p.unit or '',
        'quantity_available': p.quantity_available or 0,
        'shop_id': p.shop_id or 0,
        'shop': {
            'id': p.shop.id or 0,
            'name': p.shop.name or ''
        }
    } for p in pagination.items]
    
    return jsonify({
        'products': products,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@api_bp.route('/recommend', methods=['POST'])
@login_required
def api_recommend():
    """API endpoint for AI recommendations"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['project_description'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        project_type = data.get('project_type', '2_bedroom_house')
        custom_specs = data.get('custom_specs', {})
        
        # Generate recommendation
        recommendation = generate_full_recommendation(
            user_id=current_user.id,
            project_description=data['project_description'],
            project_type=project_type,
            custom_specs=custom_specs if custom_specs else None,
            user_lat=current_user.latitude,
            user_lon=current_user.longitude
        )
        
        return jsonify(recommendation)
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/services/search', methods=['GET'])
def search_services():
    """Search services"""
    service_type = request.args.get('type')
    min_rate = request.args.get('min_rate', type=float)
    max_rate = request.args.get('max_rate', type=float)
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build query
    services_query = Service.query.filter_by(is_available=True)
    
    if service_type:
        services_query = services_query.filter(Service.service_type == service_type)
    
    if min_rate:
        services_query = services_query.filter(Service.hourly_rate >= min_rate)
    
    if max_rate:
        services_query = services_query.filter(Service.hourly_rate <= max_rate)
    
    # Paginate
    pagination = services_query.paginate(page=page, per_page=per_page, error_out=False)
    
    services = [{
        'id': s.id or 0,
        'title': s.title or '',
        'description': s.description or '',
        'service_type': s.service_type or '',
        'hourly_rate': float(s.hourly_rate) if s.hourly_rate else 0.0,
        'rating': float(s.rating) if s.rating else 0.0,
        'years_experience': s.years_experience or 0,
        'is_available': s.is_available if s.is_available is not None else True,
        'service_area': s.service_area,
        'certifications': s.certifications,
        'portfolio_url': s.portfolio_url,
        'provider_id': s.provider_id or 0,
        'created_at': s.created_at.isoformat() if s.created_at else None,
        'updated_at': s.updated_at.isoformat() if s.updated_at else None,
        'provider': {
            'id': s.provider.id or 0,
            'name': s.provider.full_name or s.provider.username or ''
        }
    } for s in pagination.items]
    
    return jsonify({
        'services': services,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': pagination.page,
        'per_page': per_page,
    }), 200


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    try:
        from app.models import Category
        
        categories = Category.query.filter_by(is_active=True).all()
        
        categories_data = [{
            'id': cat.id or 0,
            'name': cat.name or '',
            'description': cat.description or '',
            'slug': cat.slug or '',
            'parent_id': cat.parent_id,
        } for cat in categories]
        
        return jsonify({
            'categories': categories_data,
            'count': len(categories_data)
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/login', methods=['POST'])
def api_login():
    """API endpoint for user login"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['email', 'password'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        email = data.get('email')
        password = data.get('password')
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        if not user or not user.check_password(password):
            return handle_validation_error({'credentials': 'Invalid email or password'})
        
        if not user.is_active:
            return handle_validation_error({'account': 'Account is inactive'})
        
        # Login user
        login_user(user, remember=False)
        
        # Return user data as JSON
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'address': user.address,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'user_type': user.user_type,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            }
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/register', methods=['POST'])
def api_register():
    """API endpoint for user registration"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['username', 'email', 'password'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        # Check if username already exists
        if User.query.filter_by(username=username).first():
            return jsonify({'error': 'Username already registered'}), 400
        
        # Check if email already exists
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        # Create new user
        user = User(
            username=username,
            email=email,
            full_name=data.get('fullName'),
            phone=data.get('phone'),
            address=data.get('address'),
            user_type=data.get('userType', 'customer'),
        )
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        # Login the new user
        login_user(user, remember=False)
        
        # Return user data as JSON
        return jsonify({
            'message': 'Registration successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'phone': user.phone,
                'address': user.address,
                'latitude': user.latitude,
                'longitude': user.longitude,
                'user_type': user.user_type,
                'is_active': user.is_active,
                'is_verified': user.is_verified,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            }
        }), 201
            
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/shop/<int:shop_id>/products', methods=['GET'])
def shop_products(shop_id):
    """Get all products for a specific shop"""
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return handle_not_found_error("Shop")
        
        products = Product.query.filter_by(
            shop_id=shop_id,
            is_available=True
        ).all()
        
        products_data = [{
            'id': p.id or 0,
            'name': p.name or '',
            'category': p.category or '',
            'price': float(p.price) if p.price else 0.0,
            'unit': p.unit or '',
            'quantity_available': p.quantity_available or 0,
            'shop_id': p.shop_id or 0,
            'description': p.description or ''
        } for p in products]
    
        return jsonify({
            'shop': {
                'id': shop.id or 0,
                'name': shop.name or '',
                'address': shop.address or '',
                'rating': float(shop.rating) if shop.rating else 0.0
            },
            'products': products_data,
            'count': len(products_data)
        })
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/dashboard', methods=['GET'])
@login_required
def api_user_dashboard():
    """API endpoint for user dashboard (returns JSON)"""
    try:
        # Get user's recent orders
        recent_orders_query = Order.query.filter_by(customer_id=current_user.id)\
                                         .order_by(Order.created_at.desc())\
                                         .limit(5).all()
        
        recent_orders = [{
            'id': order.id or 0,
            'order_number': order.order_number or f'ORD-{order.id or 0}',
            'total_amount': float(order.total_amount) if order.total_amount else 0.0,
            'status': order.status or 'pending',
            'payment_status': order.payment_status or 'pending',
            'customer_id': order.customer_id or 0,
            'shop_id': order.shop_id or 0,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None,
        } for order in recent_orders_query]
        
        # Get user's saved recommendations
        saved_recommendations_query = Recommendation.query.filter_by(
            user_id=current_user.id, 
            is_saved=True
        ).order_by(Recommendation.created_at.desc()).limit(5).all()
        
        saved_recommendations = [{
            'id': rec.id or 0,
            'project_type': rec.project_type or 'general',
            'project_description': rec.project_description or '',
            'total_estimated_cost': float(rec.total_estimated_cost) if rec.total_estimated_cost else None,
            'recommendation_data': rec.recommendation_data or {},
            'is_saved': rec.is_saved if rec.is_saved is not None else False,
            'user_id': rec.user_id or 0,
            'created_at': rec.created_at.isoformat() if rec.created_at else None,
            'updated_at': rec.updated_at.isoformat() if rec.updated_at else None,
        } for rec in saved_recommendations_query]
        
        # Calculate statistics
        total_orders = Order.query.filter_by(customer_id=current_user.id).count()
        total_recommendations = Recommendation.query.filter_by(user_id=current_user.id).count()
        total_spent = db.session.query(db.func.sum(Order.total_amount))\
                               .filter_by(customer_id=current_user.id).scalar() or 0
        
        return jsonify({
            'stats': {
                'total_orders': total_orders or 0,
                'total_recommendations': total_recommendations or 0,
                'total_bookings': 0,
                'total_spent': float(total_spent) if total_spent else 0.0,
            },
            'recent_orders': recent_orders,
            'saved_recommendations': saved_recommendations,
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/orders', methods=['GET'])
@login_required
def api_user_orders():
    """API endpoint for user orders (returns JSON)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        # Paginate user orders
        pagination = Order.query.filter_by(customer_id=current_user.id)\
                                .order_by(Order.created_at.desc())\
                                .paginate(page=page, per_page=per_page, error_out=False)
        
        orders = [{
            'id': order.id or 0,
            'order_number': order.order_number or f'ORD-{order.id or 0}',
            'total_amount': float(order.total_amount) if order.total_amount else 0.0,
            'status': order.status or 'pending',
            'payment_status': order.payment_status or 'pending',
            'customer_id': order.customer_id or 0,
            'shop_id': order.shop_id or 0,
            'created_at': order.created_at.isoformat() if order.created_at else None,
            'updated_at': order.updated_at.isoformat() if order.updated_at else None,
        } for order in pagination.items]
        
        return jsonify({
            'orders': orders,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/recommendations', methods=['GET'])
@login_required
def api_user_recommendations():
    """API endpoint for user recommendations (returns JSON)"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        saved_only = request.args.get('saved', type=bool)
        
        # Build query
        query = Recommendation.query.filter_by(user_id=current_user.id)
        
        if saved_only:
            query = query.filter_by(is_saved=True)
        
        # Paginate
        pagination = query.order_by(Recommendation.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )
        
        recommendations = [{
            'id': rec.id or 0,
            'project_type': rec.project_type or 'general',
            'project_description': rec.project_description or '',
            'total_estimated_cost': float(rec.total_estimated_cost) if rec.total_estimated_cost else None,
            'recommendation_data': rec.recommendation_data or {},
            'is_saved': rec.is_saved if rec.is_saved is not None else False,
            'user_id': rec.user_id or 0,
            'created_at': rec.created_at.isoformat() if rec.created_at else None,
            'updated_at': rec.updated_at.isoformat() if rec.updated_at else None,
        } for rec in pagination.items]
        
        return jsonify({
            'recommendations': recommendations,
            'total': pagination.total,
            'pages': pagination.pages,
            'current_page': pagination.page,
            'per_page': per_page,
        }), 200
    except Exception as e:
        return handle_api_error(e)


# ============================================================
# Cart API Endpoints
# ============================================================

@api_bp.route('/user/cart', methods=['GET'])
@login_required
def api_get_cart():
    """Get user's cart"""
    try:
        # Get or create cart for user
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        # Get cart items with product details
        items = []
        for item in cart.items:
            items.append({
                'id': item.id or 0,
                'product_id': item.product_id or 0,
                'quantity': item.quantity or 0,
                'price_snapshot': float(item.price_snapshot) if item.price_snapshot else 0.0,
                'subtotal': float(item.get_subtotal()) if item.get_subtotal() else 0.0,
                'product': {
                    'id': item.product.id or 0,
                    'name': item.product.name or '',
                    'category': item.product.category or '',
                    'unit': item.product.unit or '',
                    'shop_id': item.product.shop_id or 0,
                    'shop': {
                        'id': item.product.shop.id or 0,
                        'name': item.product.shop.name or '',
                    } if item.product.shop else None,
                } if item.product else None,
            })
        
        cart_total = float(cart.get_total()) if cart.get_total() else 0.0
        
        return jsonify({
            'id': cart.id or 0,
            'user_id': cart.user_id or 0,
            'items': items,
            'total': cart_total,
            'items_count': cart.get_items_count() or 0,
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/add', methods=['POST'])
@login_required
def api_add_to_cart():
    """Add product to cart"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['product_id', 'quantity'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        product_id = data.get('product_id')
        quantity = data.get('quantity', 1)
        
        if quantity <= 0:
            return handle_validation_error({'quantity': 'Quantity must be greater than 0'})
        
        # Get product
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        if not product.is_available:
            return handle_validation_error({'product': 'Product is not available'})
        
        if quantity > product.quantity_available:
            return handle_validation_error({'quantity': f'Only {product.quantity_available} available'})
        
        # Get or create cart
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user_id=current_user.id)
            db.session.add(cart)
            db.session.commit()
        
        # Check if product already in cart
        existing_item = CartItem.query.filter_by(
            cart_id=cart.id,
            product_id=product_id
        ).first()
        
        if existing_item:
            # Update quantity
            new_quantity = existing_item.quantity + quantity
            if new_quantity > product.quantity_available:
                return handle_validation_error({'quantity': f'Only {product.quantity_available} available'})
            existing_item.quantity = new_quantity
        else:
            # Create new cart item
            cart_item = CartItem(
                cart_id=cart.id,
                product_id=product_id,
                quantity=quantity,
                price_snapshot=product.price
            )
            db.session.add(cart_item)
        
        db.session.commit()
        
        # Return updated cart
        return api_get_cart()
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/item/<int:item_id>/update', methods=['PUT'])
@login_required
def api_update_cart_item(item_id):
    """Update cart item quantity"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['quantity'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        quantity = data.get('quantity')
        
        if quantity <= 0:
            return handle_validation_error({'quantity': 'Quantity must be greater than 0'})
        
        # Get cart item
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            return handle_not_found_error("Cart item")
        
        # Verify cart belongs to user
        cart = cart_item.cart
        if cart.user_id != current_user.id:
            return handle_permission_error("Cart does not belong to user")
        
        # Check product availability
        product = cart_item.product
        if quantity > product.quantity_available:
            return handle_validation_error({'quantity': f'Only {product.quantity_available} available'})
        
        # Update quantity
        cart_item.quantity = quantity
        db.session.commit()
        
        # Return updated cart
        return api_get_cart()
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/item/<int:item_id>/remove', methods=['DELETE'])
@login_required
def api_remove_cart_item(item_id):
    """Remove item from cart"""
    try:
        # Get cart item
        cart_item = CartItem.query.get(item_id)
        if not cart_item:
            return handle_not_found_error("Cart item")
        
        # Verify cart belongs to user
        cart = cart_item.cart
        if cart.user_id != current_user.id:
            return handle_permission_error("Cart does not belong to user")
        
        # Remove item
        db.session.delete(cart_item)
        db.session.commit()
        
        # Return updated cart
        return api_get_cart()
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/clear', methods=['POST'])
@login_required
def api_clear_cart():
    """Clear all items from cart"""
    try:
        # Get user's cart
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            return jsonify({'message': 'Cart is already empty'}), 200
        
        # Remove all items
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        
        return jsonify({'message': 'Cart cleared successfully'}), 200
    except Exception as e:
        return handle_api_error(e)


# ============================================================
# Checkout API Endpoints
# ============================================================

@api_bp.route('/user/checkout/place-order', methods=['POST'])
@login_required
def api_place_order():
    """Create order from cart"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['delivery_address'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        delivery_address = data.get('delivery_address')
        delivery_notes = data.get('delivery_notes', '')
        payment_method = data.get('payment_method', 'cash_on_delivery')
        
        # Get user's cart
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart or cart.is_empty():
            return handle_validation_error({'cart': 'Cart is empty'})
        
        # Group items by shop
        items_by_shop = {}
        for item in cart.items:
            shop_id = item.product.shop_id
            if shop_id not in items_by_shop:
                items_by_shop[shop_id] = []
            items_by_shop[shop_id].append(item)
        
        created_orders = []
        
        # Create order for each shop
        for shop_id, items in items_by_shop.items():
            shop = Shop.query.get(shop_id)
            if not shop:
                continue
            
            # Calculate order total
            order_total = Decimal('0.0')
            for item in items:
                subtotal = item.get_subtotal()
                if subtotal:
                    order_total += subtotal
            
            # Add tax (18%)
            tax = order_total * Decimal('0.18')
            total_with_tax = order_total + tax
            
            # Generate order number
            import random
            order_number = f'ORD-{current_user.id}-{shop_id}-{random.randint(1000, 9999)}'
            
            # Create order
            order = Order(
                order_number=order_number,
                customer_id=current_user.id,
                shop_id=shop_id,
                total_amount=total_with_tax,
                delivery_address=delivery_address,
                delivery_notes=delivery_notes,
                payment_method=payment_method,
                status='pending',
                payment_status='pending'
            )
            db.session.add(order)
            db.session.flush()  # Get order.id
            
            # Create order items
            for item in items:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=item.price_snapshot,
                    total_price=item.get_subtotal()
                )
                db.session.add(order_item)
                
                # Update product quantity
                product = item.product
                product.quantity_available -= item.quantity
                if product.quantity_available < 0:
                    product.quantity_available = 0
            
            created_orders.append({
                'id': order.id or 0,
                'order_number': order.order_number or '',
                'shop_id': shop_id or 0,
                'shop_name': shop.name or '',
                'total_amount': float(total_with_tax),
                'status': order.status or 'pending',
            })
        
        # Clear cart
        CartItem.query.filter_by(cart_id=cart.id).delete()
        db.session.commit()
        
        return jsonify({
            'message': 'Order placed successfully',
            'orders': created_orders
        }), 201
    except Exception as e:
        return handle_api_error(e)
