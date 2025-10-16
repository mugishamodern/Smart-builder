from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import Shop, Product, Service
from app.extensions import db
from app.ai.recommender import generate_full_recommendation

api_bp = Blueprint('api', __name__)


@api_bp.route('/shops/nearby', methods=['GET'])
def nearby_shops():
    """Get shops near a location"""
    lat = request.args.get('lat', type=float)
    lon = request.args.get('lon', type=float)
    radius = request.args.get('radius', 10, type=float)  # km
    
    if not lat or not lon:
        return jsonify({'error': 'Latitude and longitude required'}), 400
    
    # Get all verified shops
    shops = Shop.query.filter_by(is_verified=True).all()
    
    # Filter by distance
    nearby = []
    for shop in shops:
        distance = shop.distance_to(lat, lon)
        if distance <= radius:
            nearby.append({
                'id': shop.id,
                'name': shop.name,
                'address': shop.address,
                'distance_km': round(distance, 2),
                'rating': shop.rating,
                'phone': shop.phone
            })
    
    # Sort by distance
    nearby.sort(key=lambda x: x['distance_km'])
    
    return jsonify({
        'shops': nearby,
        'count': len(nearby)
    })


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
            (Product.name.ilike(f'%{query}%')) | (Product.description.ilike(f'%{query}%'))
        )
    
    if category:
        products_query = products_query.filter_by(category=category)
    
    if min_price:
        products_query = products_query.filter(Product.price >= min_price)
    
    if max_price:
        products_query = products_query.filter(Product.price <= max_price)
    
    # Paginate
    pagination = products_query.paginate(page=page, per_page=per_page, error_out=False)
    
    products = [{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'price': p.price,
        'unit': p.unit,
        'quantity_available': p.quantity_available,
        'shop': {
            'id': p.shop.id,
            'name': p.shop.name
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
    data = request.get_json()
    
    if not data or 'project_description' not in data:
        return jsonify({'error': 'Project description required'}), 400
    
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
        services_query = services_query.filter_by(service_type=service_type)
    
    if min_rate:
        services_query = services_query.filter(Service.hourly_rate >= min_rate)
    
    if max_rate:
        services_query = services_query.filter(Service.hourly_rate <= max_rate)
    
    # Paginate
    pagination = services_query.paginate(page=page, per_page=per_page, error_out=False)
    
    services = [{
        'id': s.id,
        'title': s.title,
        'service_type': s.service_type,
        'hourly_rate': s.hourly_rate,
        'rating': s.rating,
        'years_experience': s.years_experience,
        'provider': {
            'name': s.provider.full_name or s.provider.username
        }
    } for s in pagination.items]
    
    return jsonify({
        'services': services,
        'total': pagination.total,
        'pages': pagination.pages,
        'current_page': page
    })


@api_bp.route('/categories', methods=['GET'])
def get_categories():
    """Get all product categories"""
    categories = db.session.query(Product.category).distinct().all()
    
    category_list = [c[0] for c in categories]
    
    return jsonify({
        'categories': category_list,
        'count': len(category_list)
    })


@api_bp.route('/shop/<int:shop_id>/products', methods=['GET'])
def shop_products(shop_id):
    """Get all products for a specific shop"""
    shop = Shop.query.get_or_404(shop_id)
    
    products = Product.query.filter_by(
        shop_id=shop_id,
        is_available=True
    ).all()
    
    products_data = [{
        'id': p.id,
        'name': p.name,
        'category': p.category,
        'price': p.price,
        'unit': p.unit,
        'quantity_available': p.quantity_available,
        'description': p.description
    } for p in products]
    
    return jsonify({
        'shop': {
            'id': shop.id,
            'name': shop.name,
            'address': shop.address,
            'rating': shop.rating
        },
        'products': products_data,
        'count': len(products_data)
    })