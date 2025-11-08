from flask import jsonify, request, session
from flask_login import login_required, current_user, login_user
from app.models import (
    Shop, Product, Service, User, Order, Recommendation, Cart, CartItem,
    Comparison, Review, Address, Token, ProductImage, Wishlist, StockNotification,
    SearchHistory, TrendingSearch, OrderStatus
)
from app.extensions import db, limiter
from app.ai.recommender import generate_full_recommendation
from app.blueprints.api import api_bp
from app.utils.error_handlers import (
    handle_api_error, handle_validation_error, handle_permission_error,
    handle_not_found_error, validate_required_fields, validate_json_request
)
from app.utils.security import (
    sanitize_string, validate_password_strength,
    LoginSchema, RegistrationSchema, PasswordResetRequestSchema,
    PasswordResetSchema, EmailVerificationSchema
)
from app.services.email_service import EmailService
from app.services.two_factor_service import TwoFactorService
from app.utils.cart_utils import merge_guest_cart_to_user
from marshmallow import ValidationError
from decimal import Decimal

# Rate limiting decorators
rate_limit_login = limiter.limit("5 per minute")
rate_limit_register = limiter.limit("3 per hour")
rate_limit_password_reset = limiter.limit("3 per hour")
rate_limit_email_verification = limiter.limit("5 per hour")


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
    """Search products with advanced filters, sorting, and search history tracking"""
    from sqlalchemy import func, desc, asc
    from math import radians, sin, cos, sqrt, atan2
    from flask_login import current_user
    
    query = request.args.get('q', '')
    search_type = 'products'
    category = request.args.get('category')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    min_rating = request.args.get('min_rating', type=float)
    shop_verified = request.args.get('shop_verified', type=bool, default=None)
    user_lat = request.args.get('lat', type=float)
    user_lon = request.args.get('lon', type=float)
    max_distance = request.args.get('max_distance', type=float)  # in km
    sort_by = request.args.get('sort_by', 'relevance')  # relevance, price_asc, price_desc, rating, distance
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    
    # Build base query with joins
    products_query = db.session.query(Product, Shop).join(Shop, Product.shop_id == Shop.id).filter(
        Product.is_available == True,
        Shop.is_active == True
    )
    
    # Text search
    if query:
        products_query = products_query.filter(
            (Product.name.ilike(f'%{query}%')) | 
            (Product.description.ilike(f'%{query}%'))
        )
    
    # Category filter
    if category:
        products_query = products_query.filter(Product.category == category)
    
    # Price filters
    if min_price:
        products_query = products_query.filter(Product.price >= min_price)
    
    if max_price:
        products_query = products_query.filter(Product.price <= max_price)
    
    # Shop rating filter
    if min_rating:
        products_query = products_query.filter(Shop.rating >= min_rating)
    
    # Shop verification filter
    if shop_verified is not None:
        products_query = products_query.filter(Shop.is_verified == shop_verified)
    
    # Note: Distance filtering will be done after fetching results
    # for better compatibility with different databases
    
    # Sorting
    if sort_by == 'price_asc':
        products_query = products_query.order_by(Product.price.asc())
    elif sort_by == 'price_desc':
        products_query = products_query.order_by(Product.price.desc())
    elif sort_by == 'rating':
        products_query = products_query.order_by(Shop.rating.desc(), Shop.total_reviews.desc())
    elif sort_by == 'distance' and user_lat and user_lon:
        # Order by distance (calculate in Python after fetching)
        # For now, just order by shop location
        products_query = products_query.order_by(Shop.latitude, Shop.longitude)
    else:
        # Default: relevance (by shop rating and review count for now)
        products_query = products_query.order_by(Shop.rating.desc(), Shop.total_reviews.desc())
    
    # Paginate
    pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    
    # Build response with distance if user location provided
    products = []
    for product, shop in pagination.items:
        # Calculate distance if user location provided
        distance_km = None
        if user_lat and user_lon and shop.latitude and shop.longitude:
            # Haversine formula
            lat1, lon1 = radians(user_lat), radians(user_lon)
            lat2, lon2 = radians(float(shop.latitude)), radians(float(shop.longitude))
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
            c = 2 * atan2(sqrt(a), sqrt(1 - a))
            distance_km = 6371 * c  # Earth radius in km
            
            # Filter by max_distance if specified
            if max_distance and distance_km > max_distance:
                continue  # Skip products outside max distance
        
        product_data = {
            'id': product.id or 0,
            'name': product.name or '',
            'category': product.category or '',
            'price': float(product.price) if product.price else 0.0,
            'unit': product.unit or '',
            'quantity_available': product.quantity_available or 0,
            'shop_id': product.shop_id or 0,
            'shop': {
                'id': shop.id or 0,
                'name': shop.name or '',
                'rating': float(shop.rating) if shop.rating else 0.0,
                'total_reviews': shop.total_reviews or 0,
                'is_verified': shop.is_verified if shop.is_verified is not None else False,
                'address': shop.address or '',
                'latitude': float(shop.latitude) if shop.latitude else None,
                'longitude': float(shop.longitude) if shop.longitude else None,
            }
        }
        
        if distance_km is not None:
            product_data['distance_km'] = round(distance_km, 2)
        
        products.append(product_data)
    
    # Re-sort by distance if requested (after calculating distances)
    if sort_by == 'distance' and user_lat and user_lon:
        products.sort(key=lambda p: p.get('distance_km', float('inf')))
    
    # Track search history
    if query:
        try:
            # Save search history for authenticated users
            if current_user.is_authenticated:
                search_history = SearchHistory(
                    user_id=current_user.id,
                    query=query,
                    search_type=search_type,
                    results_count=len(products)
                )
                db.session.add(search_history)
            
            # Update trending searches
            trending = TrendingSearch.query.filter_by(
                query=query.lower().strip(),
                search_type=search_type
            ).first()
            
            if trending:
                trending.increment()
            else:
                trending = TrendingSearch(
                    query=query.lower().strip(),
                    search_type=search_type,
                    count=1
                )
                db.session.add(trending)
            
            db.session.commit()
        except Exception as e:
            from flask import current_app
            current_app.logger.error(f'Error tracking search: {str(e)}')
            db.session.rollback()
    
    return jsonify({
        'products': products,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page,
        'per_page': per_page
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
@rate_limit_login
def api_login():
    """API endpoint for user login with security enhancements"""
    try:
        # Validate JSON request
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        # Validate with Marshmallow schema
        schema = LoginSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return handle_validation_error(err.messages)
        
        # Sanitize inputs
        email = sanitize_string(validated_data.get('email', ''), max_length=120).lower()
        password = validated_data.get('password', '')
        remember_me = validated_data.get('remember_me', False)
        
        # Find user
        user = User.query.filter_by(email=email).first()
        
        # Check if account is locked
        if user and user.is_account_locked():
            return jsonify({
                'error': 'Account locked',
                'message': 'Account is temporarily locked due to multiple failed login attempts. Please try again later or reset your password.'
            }), 423
        
        # Validate credentials
        if not user or not user.check_password(password):
            if user:
                user.increment_failed_login()
            return handle_validation_error({'credentials': 'Invalid email or password'})
        
        if not user.is_active:
            return handle_validation_error({'account': 'Account is inactive'})
        
        # Check if 2FA is enabled
        if user.two_factor_enabled:
            two_factor_code = data.get('two_factor_code')
            if not two_factor_code:
                return jsonify({
                    'error': '2FA required',
                    'message': 'Two-Factor Authentication is enabled. Please provide verification code.',
                    'requires_2fa': True
                }), 200
            
            if not TwoFactorService.verify_code(user, two_factor_code):
                return handle_validation_error({'two_factor_code': 'Invalid verification code'})
        
        # Reset failed login attempts on successful login
        user.reset_failed_login_attempts()
        
        # Get session ID from request for cart merging
        session_id = request.headers.get('X-Session-ID') or request.cookies.get('session_id')
        
        # Login user
        login_user(user, remember=remember_me)
        
        # Merge guest cart with user cart
        if session_id:
            merge_guest_cart_to_user(user.id, session_id)
        
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
                'email_verified': user.email_verified,
                'two_factor_enabled': user.two_factor_enabled,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            }
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/register', methods=['POST'])
@rate_limit_register
def api_register():
    """API endpoint for user registration with security enhancements"""
    try:
        # Validate JSON request
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        # Validate with Marshmallow schema
        schema = RegistrationSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return handle_validation_error(err.messages)
        
        # Sanitize inputs
        username = sanitize_string(validated_data.get('username', ''), max_length=20)
        email = sanitize_string(validated_data.get('email', ''), max_length=120).lower()
        password = validated_data.get('password', '')
        full_name = sanitize_string(validated_data.get('full_name', ''), max_length=100)
        phone = sanitize_string(validated_data.get('phone', ''), max_length=20) if validated_data.get('phone') else None
        address = sanitize_string(validated_data.get('address', ''), max_length=500) if validated_data.get('address') else None
        user_type = validated_data.get('user_type', 'customer')
        
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            return handle_validation_error({'password': error_msg})
        
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
            full_name=full_name,
            phone=phone,
            address=address,
            user_type=user_type,
        )
        user.set_password(password)
        user.email_verified = False  # Require email verification
        
        db.session.add(user)
        db.session.commit()
        
        # Generate email verification token
        token = Token.generate_token(user.id, 'email_verification', expires_in_hours=48)
        
        # Send verification email
        EmailService.send_verification_email(user, token.token)
        
        # Login the new user
        login_user(user, remember=False)
        
        # Return user data as JSON
        return jsonify({
            'message': 'Registration successful! Please check your email to verify your account.',
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
                'email_verified': user.email_verified,
                'created_at': user.created_at.isoformat() if user.created_at else None,
                'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            }
        }), 201
            
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/forgot-password', methods=['POST'])
@rate_limit_password_reset
def api_forgot_password():
    """API endpoint for password reset request"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        schema = PasswordResetRequestSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return handle_validation_error(err.messages)
        
        email = sanitize_string(validated_data.get('email', ''), max_length=120).lower()
        
        user = User.query.filter_by(email=email).first()
        
        # Always show success message to prevent email enumeration
        if user:
            token = Token.generate_token(user.id, 'password_reset', expires_in_hours=1)
            EmailService.send_password_reset_email(user, token.token)
        
        return jsonify({
            'message': 'If an account with that email exists, a password reset link has been sent.'
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/reset-password', methods=['POST'])
@rate_limit_password_reset
def api_reset_password():
    """API endpoint for password reset confirmation"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        schema = PasswordResetSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return handle_validation_error(err.messages)
        
        token = validated_data.get('token')
        password = validated_data.get('password')
        
        # Validate token
        token_obj = Token.validate_token(token, 'password_reset')
        if not token_obj:
            return handle_validation_error({'token': 'Invalid or expired password reset link'})
        
        user = token_obj.user
        
        # Validate password strength
        is_valid, error_msg = validate_password_strength(password)
        if not is_valid:
            return handle_validation_error({'password': error_msg})
        
        # Update password
        user.set_password(password)
        user.unlock_account()
        
        # Mark token as used
        token_obj.mark_as_used()
        
        db.session.commit()
        
        return jsonify({
            'message': 'Password reset successful! Please log in with your new password.'
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/verify-email', methods=['POST'])
@rate_limit_email_verification
def api_verify_email():
    """API endpoint for email verification"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        schema = EmailVerificationSchema()
        try:
            validated_data = schema.load(data)
        except ValidationError as err:
            return handle_validation_error(err.messages)
        
        token = validated_data.get('token')
        
        # Validate token
        token_obj = Token.validate_token(token, 'email_verification')
        if not token_obj:
            return handle_validation_error({'token': 'Invalid or expired verification link'})
        
        user = token_obj.user
        
        # Verify email
        user.verify_email()
        
        # Mark token as used
        token_obj.mark_as_used()
        
        return jsonify({
            'message': 'Email verified successfully!',
            'user': {
                'id': user.id,
                'email_verified': user.email_verified
            }
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/resend-verification', methods=['POST'])
@login_required
@rate_limit_email_verification
def api_resend_verification():
    """API endpoint to resend email verification"""
    try:
        if current_user.email_verified:
            return jsonify({
                'message': 'Your email is already verified.'
            }), 200
        
        # Generate new verification token
        token = Token.generate_token(current_user.id, 'email_verification', expires_in_hours=48)
        
        # Send verification email
        EmailService.send_verification_email(current_user, token.token)
        
        return jsonify({
            'message': 'Verification email sent! Please check your inbox.'
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/enable-2fa', methods=['POST'])
@login_required
def api_enable_2fa():
    """API endpoint to enable Two-Factor Authentication"""
    try:
        if current_user.two_factor_enabled:
            return jsonify({
                'message': '2FA is already enabled for your account.'
            }), 200
        
        # Generate secret and QR code
        secret, qr_code = TwoFactorService.enable_2fa(current_user)
        
        return jsonify({
            'message': '2FA enabled successfully! Please scan the QR code with your authenticator app.',
            'qr_code': qr_code,
            'secret': secret
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/auth/disable-2fa', methods=['POST'])
@login_required
def api_disable_2fa():
    """API endpoint to disable Two-Factor Authentication"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        password = data.get('password', '')
        
        if not current_user.check_password(password):
            return handle_validation_error({'password': 'Incorrect password'})
        
        if not current_user.two_factor_enabled:
            return jsonify({
                'message': '2FA is not enabled for your account.'
            }), 200
        
        TwoFactorService.disable_2fa(current_user)
        
        return jsonify({
            'message': '2FA disabled successfully.'
        }), 200
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


@api_bp.route('/comparisons', methods=['GET'])
@login_required
def api_get_comparisons():
    """Get all products in user's comparison list"""
    try:
        comparisons = Comparison.query.filter_by(user_id=current_user.id).all()
        
        return jsonify({
            'success': True,
            'comparisons': [comp.to_dict() for comp in comparisons]
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/comparisons/add', methods=['POST'])
@login_required
def api_add_to_comparison():
    """Add product to comparison list"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['product_id'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        product_id = data.get('product_id')
        
        # Check if product exists
        product = Product.query.get(product_id)
        if not product:
            return handle_not_found_error("Product")
        
        # Check if already in comparison
        existing = Comparison.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if existing:
            return jsonify({
                'success': False,
                'message': 'Product already in comparison list'
            }), 400
        
        # Add to comparison
        comparison = Comparison(
            user_id=current_user.id,
            product_id=product_id
        )
        db.session.add(comparison)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'comparison': comparison.to_dict()
        }), 201
    
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/comparisons/<int:product_id>/remove', methods=['DELETE'])
@login_required
def api_remove_from_comparison(product_id):
    """Remove product from comparison list"""
    try:
        comparison = Comparison.query.filter_by(
            user_id=current_user.id,
            product_id=product_id
        ).first()
        
        if not comparison:
            return handle_not_found_error("Comparison")
        
        db.session.delete(comparison)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Product removed from comparison'
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/comparisons/clear', methods=['DELETE'])
@login_required
def api_clear_comparisons():
    """Clear all products from comparison list"""
    try:
        comparisons = Comparison.query.filter_by(user_id=current_user.id).all()
        
        for comp in comparisons:
            db.session.delete(comp)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Comparison list cleared'
        }), 200
    
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
        status_filter = request.args.get('status', '')
        
        # Build query
        query = Order.query.filter_by(customer_id=current_user.id)
        
        # Apply status filter if provided
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        # Paginate user orders
        pagination = query.order_by(Order.created_at.desc())\
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


@api_bp.route('/orders/<int:order_id>/cancel', methods=['POST'])
@login_required
def api_cancel_order(order_id):
    """Cancel an order (only if status is pending)"""
    try:
        order = Order.query.get_or_404(order_id)
        
        # Check if user owns this order
        if order.customer_id != current_user.id:
            return handle_permission_error("You can only cancel your own orders")
        
        # Check if order can be cancelled
        if order.status not in ['pending', 'confirmed']:
            return handle_validation_error({
                'status': f'Order with status "{order.status}" cannot be cancelled'
            })
        
        # Update order status
        order.status = 'cancelled'
        order.payment_status = 'refunded' if order.payment_status == 'paid' else 'pending'
        
        # Restore product quantities if needed
        for item in order.items:
            if item.product:
                item.product.quantity_available += item.quantity
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Order cancelled successfully',
            'order': {
                'id': order.id,
                'order_number': order.order_number,
                'status': order.status,
            }
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/reviews/submit', methods=['POST'])
@login_required
def api_submit_review():
    """Submit a review for a shop or product"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['shop_id', 'rating'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        shop_id = data.get('shop_id')
        product_id = data.get('product_id')  # Optional
        rating = float(data.get('rating', 0))
        comment = data.get('comment', '').strip()
        
        # Validate rating
        if rating < 1 or rating > 5:
            return handle_validation_error({'rating': 'Rating must be between 1 and 5'})
        
        # Verify shop exists
        shop = Shop.query.get(shop_id)
        if not shop:
            return handle_not_found_error("Shop")
        
        # Check if user has already reviewed this shop/product
        existing_review = Review.query.filter_by(
            user_id=current_user.id,
            shop_id=shop_id,
            product_id=product_id if product_id else None
        ).first()
        
        if existing_review:
            # Update existing review
            existing_review.rating = rating
            existing_review.comment = comment
            db.session.commit()
            review = existing_review
        else:
            # Create new review
            review = Review(
                user_id=current_user.id,
                shop_id=shop_id,
                product_id=product_id,
                rating=rating,
                comment=comment,
                is_verified=False,  # Can be set to True if user has order from this shop
                is_approved=True
            )
            db.session.add(review)
            db.session.commit()
            
            # Update shop rating
            from sqlalchemy import func
            shop_reviews = Review.query.filter_by(shop_id=shop_id, is_approved=True).all()
            if shop_reviews:
                avg_rating = sum(r.rating for r in shop_reviews) / len(shop_reviews)
                shop.rating = round(avg_rating, 2)
                shop.total_reviews = len(shop_reviews)
                db.session.commit()
        
        return jsonify({
            'success': True,
            'review': {
                'id': review.id,
                'user_id': review.user_id,
                'shop_id': review.shop_id,
                'product_id': review.product_id,
                'rating': review.rating,
                'comment': review.comment,
                'created_at': review.created_at.isoformat() if review.created_at else None,
            }
        }), 201
    
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/shop/<int:shop_id>/reviews', methods=['GET'])
def api_get_shop_reviews(shop_id):
    """Get reviews for a shop"""
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return handle_not_found_error("Shop")
        
        reviews = Review.query.filter_by(
            shop_id=shop_id,
            is_approved=True
        ).order_by(Review.created_at.desc()).all()
        
        reviews_data = [{
            'id': r.id,
            'user_id': r.user_id,
            'rating': r.rating,
            'comment': r.comment,
            'is_verified': r.is_verified,
            'created_at': r.created_at.isoformat() if r.created_at else None,
            'user': {
                'id': r.user.id,
                'username': r.user.username,
                'full_name': r.user.full_name,
            } if r.user else None,
        } for r in reviews]
        
        return jsonify({
            'success': True,
            'reviews': reviews_data
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/recommendations/<int:recommendation_id>/save', methods=['PUT'])
@login_required
def api_save_recommendation(recommendation_id):
    """Save or unsave a recommendation"""
    try:
        recommendation = Recommendation.query.get_or_404(recommendation_id)
        
        # Check if user owns this recommendation
        if recommendation.user_id != current_user.id:
            return handle_permission_error("You can only save your own recommendations")
        
        # Toggle save status
        recommendation.is_saved = not recommendation.is_saved
        db.session.commit()
        
        return jsonify({
            'success': True,
            'is_saved': recommendation.is_saved,
            'message': 'Recommendation saved' if recommendation.is_saved else 'Recommendation unsaved'
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/recommendations/<int:recommendation_id>', methods=['DELETE'])
@login_required
def api_delete_recommendation(recommendation_id):
    """Delete a recommendation"""
    try:
        recommendation = Recommendation.query.get_or_404(recommendation_id)
        
        # Check if user owns this recommendation
        if recommendation.user_id != current_user.id:
            return handle_permission_error("You can only delete your own recommendations")
        
        db.session.delete(recommendation)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Recommendation deleted successfully'
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
# Address Book API Endpoints
# ============================================================

@api_bp.route('/user/addresses', methods=['GET'])
@login_required
def api_get_addresses():
    """Get all addresses for the current user"""
    try:
        addresses = Address.query.filter_by(user_id=current_user.id).order_by(
            Address.is_default.desc(), Address.created_at.desc()
        ).all()
        
        addresses_data = [addr.to_dict() for addr in addresses]
        
        return jsonify({
            'success': True,
            'addresses': addresses_data
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/addresses', methods=['POST'])
@login_required
def api_create_address():
    """Create a new address"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, [
            'label', 'full_name', 'phone', 'address_line1', 'city', 'state'
        ])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        # If this is set as default, unset other defaults
        is_default = data.get('is_default', False)
        if is_default:
            Address.query.filter_by(user_id=current_user.id, is_default=True).update(
                {'is_default': False}
            )
        
        # Create new address
        address = Address(
            user_id=current_user.id,
            label=data.get('label'),
            full_name=data.get('full_name'),
            phone=data.get('phone'),
            address_line1=data.get('address_line1'),
            address_line2=data.get('address_line2'),
            city=data.get('city'),
            state=data.get('state'),
            postal_code=data.get('postal_code'),
            country=data.get('country', 'Uganda'),
            is_default=is_default
        )
        db.session.add(address)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Address created successfully',
            'address': address.to_dict()
        }), 201
    except Exception as e:
        db.session.rollback()
        return handle_api_error(e)


@api_bp.route('/user/addresses/<int:address_id>', methods=['PUT'])
@login_required
def api_update_address(address_id):
    """Update an existing address"""
    try:
        address = Address.query.filter_by(
            id=address_id,
            user_id=current_user.id
        ).first_or_404()
        
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        # Update fields
        if 'label' in data:
            address.label = data.get('label')
        if 'full_name' in data:
            address.full_name = data.get('full_name')
        if 'phone' in data:
            address.phone = data.get('phone')
        if 'address_line1' in data:
            address.address_line1 = data.get('address_line1')
        if 'address_line2' in data:
            address.address_line2 = data.get('address_line2')
        if 'city' in data:
            address.city = data.get('city')
        if 'state' in data:
            address.state = data.get('state')
        if 'postal_code' in data:
            address.postal_code = data.get('postal_code')
        if 'country' in data:
            address.country = data.get('country')
        
        # Handle default flag
        is_default = data.get('is_default', False)
        if is_default and not address.is_default:
            # Unset other defaults
            Address.query.filter_by(user_id=current_user.id, is_default=True).update(
                {'is_default': False}
            )
            address.is_default = True
        elif not is_default and address.is_default:
            address.is_default = False
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Address updated successfully',
            'address': address.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return handle_api_error(e)


@api_bp.route('/user/addresses/<int:address_id>', methods=['DELETE'])
@login_required
def api_delete_address(address_id):
    """Delete an address"""
    try:
        address = Address.query.filter_by(
            id=address_id,
            user_id=current_user.id
        ).first_or_404()
        
        db.session.delete(address)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Address deleted successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return handle_api_error(e)


@api_bp.route('/user/addresses/<int:address_id>/set-default', methods=['PUT'])
@login_required
def api_set_default_address(address_id):
    """Set an address as default"""
    try:
        address = Address.query.filter_by(
            id=address_id,
            user_id=current_user.id
        ).first_or_404()
        
        # Unset other defaults
        Address.query.filter_by(user_id=current_user.id, is_default=True).update(
            {'is_default': False}
        )
        
        # Set this as default
        address.is_default = True
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Default address updated successfully',
            'address': address.to_dict()
        }), 200
    except Exception as e:
        db.session.rollback()
        return handle_api_error(e)


# ============================================================
# Cart API Endpoints
# ============================================================

@api_bp.route('/user/cart', methods=['GET'])
@login_required
def api_get_cart():
    """Get user's active cart (not saved)"""
    try:
        # Get or create active cart for user (not saved)
        cart = Cart.query.filter_by(user_id=current_user.id, is_saved=False).first()
        if not cart:
            cart = Cart(user_id=current_user.id, is_saved=False)
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
        
        # Get or create active cart (not saved)
        cart = Cart.query.filter_by(user_id=current_user.id, is_saved=False).first()
        if not cart:
            cart = Cart(user_id=current_user.id, is_saved=False)
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


@api_bp.route('/user/cart/save', methods=['PUT'])
@login_required
def api_save_cart():
    """Save current cart for later (creates new active cart)"""
    try:
        cart = Cart.query.filter_by(user_id=current_user.id, is_saved=False).first()
        if not cart:
            return jsonify({'message': 'Cart not found'}), 404
        
        if cart.is_empty():
            return handle_validation_error({'cart': 'Cannot save empty cart'})
        
        # Mark current cart as saved
        cart.is_saved = True
        
        # Create new active cart for continued shopping
        new_cart = Cart(user_id=current_user.id, is_saved=False)
        db.session.add(new_cart)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Cart saved successfully. You can continue shopping with a new cart.'
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/saved', methods=['GET'])
@login_required
def api_get_saved_carts():
    """Get all saved carts for user"""
    try:
        saved_carts = Cart.query.filter_by(
            user_id=current_user.id,
            is_saved=True
        ).all()
        
        carts_data = []
        for cart in saved_carts:
            items = []
            for item in cart.items:
                items.append({
                    'id': item.id or 0,
                    'product_id': item.product_id or 0,
                    'quantity': item.quantity or 0,
                    'price_snapshot': float(item.price_snapshot) if item.price_snapshot else 0.0,
                    'product': {
                        'id': item.product.id or 0,
                        'name': item.product.name or '',
                        'shop_name': item.product.shop.name if item.product.shop else '',
                    } if item.product else None,
                })
            
            carts_data.append({
                'id': cart.id or 0,
                'saved_at': cart.updated_at.isoformat() if cart.updated_at else None,
                'items_count': cart.get_items_count() or 0,
                'total': float(cart.get_total()) if cart.get_total() else 0.0,
                'items': items
            })
        
        return jsonify({
            'success': True,
            'saved_carts': carts_data
        }), 200
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/restore/<int:cart_id>', methods=['POST'])
@login_required
def api_restore_cart(cart_id):
    """Restore a saved cart (merge with current cart or replace)"""
    try:
        saved_cart = Cart.query.filter_by(
            id=cart_id,
            user_id=current_user.id,
            is_saved=True
        ).first()
        
        if not saved_cart:
            return handle_not_found_error("Saved cart")
        
        # Get or create current active cart
        current_cart = Cart.query.filter_by(
            user_id=current_user.id,
            is_saved=False
        ).first()
        
        if not current_cart:
            current_cart = Cart(user_id=current_user.id, is_saved=False)
            db.session.add(current_cart)
            db.session.flush()
        
        # Merge items from saved cart
        for saved_item in saved_cart.items:
            # Check if product still exists and is available
            product = saved_item.product
            if not product or not product.is_available:
                continue
            
            # Check if item already in current cart
            existing_item = CartItem.query.filter_by(
                cart_id=current_cart.id,
                product_id=saved_item.product_id
            ).first()
            
            if existing_item:
                # Update quantity (take max of current and saved)
                existing_item.quantity = max(existing_item.quantity, saved_item.quantity)
                existing_item.price_snapshot = product.price  # Update price
            else:
                # Add new item
                new_item = CartItem(
                    cart_id=current_cart.id,
                    product_id=saved_item.product_id,
                    quantity=saved_item.quantity,
                    price_snapshot=product.price
                )
                db.session.add(new_item)
        
        db.session.commit()
        
        # Return updated cart
        return api_get_cart()
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/user/cart/<int:cart_id>/delete', methods=['DELETE'])
@login_required
def api_delete_saved_cart(cart_id):
    """Delete a saved cart"""
    try:
        saved_cart = Cart.query.filter_by(
            id=cart_id,
            user_id=current_user.id,
            is_saved=True
        ).first()
        
        if not saved_cart:
            return handle_not_found_error("Saved cart")
        
        # Delete the cart (cascade will delete items)
        db.session.delete(saved_cart)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Saved cart deleted successfully'
        }), 200
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
