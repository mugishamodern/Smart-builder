from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.blueprints.shop import shop_bp
from app.models import Shop, Product, Order
from app.extensions import db
from app.utils.error_handlers import handle_api_error, handle_permission_error


@shop_bp.route('/dashboard')
@login_required
def dashboard():
    """
    Shop owner dashboard.
    
    Displays shop management interface with recent orders,
    shop statistics, and management options.
    
    Returns:
        str: Rendered dashboard template with shop data
    """
    # Get user's shops
    shops = Shop.query.filter_by(owner_id=current_user.id).all()
    
    # Get recent orders for user's shops
    recent_orders = []
    for shop in shops:
        orders = Order.query.filter_by(shop_id=shop.id)\
                          .order_by(Order.created_at.desc())\
                          .limit(3).all()
        recent_orders.extend(orders)
    
    # Sort by creation date
    recent_orders.sort(key=lambda x: x.created_at, reverse=True)
    recent_orders = recent_orders[:10]
    
    return render_template('shop/dashboard.html', 
                         shops=shops,
                         recent_orders=recent_orders)


@shop_bp.route('/register', methods=['GET', 'POST'])
@login_required
def register_shop():
    """Register a new shop"""
    if request.method == 'POST':
        # Create new shop
        shop = Shop(
            name=request.form.get('name'),
            description=request.form.get('description'),
            address=request.form.get('address'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            latitude=request.form.get('latitude', type=float),
            longitude=request.form.get('longitude', type=float),
            owner_id=current_user.id
        )
        
        db.session.add(shop)
        db.session.commit()
        
        flash('Shop registered successfully!', 'success')
        return redirect(url_for('shop.dashboard'))
    
    return render_template('shop/register.html')


@shop_bp.route('/<int:shop_id>')
def shop_detail(shop_id):
    """Shop detail page"""
    shop = Shop.query.get_or_404(shop_id)
    products = Product.query.filter_by(shop_id=shop_id, is_available=True).all()
    
    return render_template('shop/detail.html', shop=shop, products=products)


@shop_bp.route('/<int:shop_id>/inventory')
@login_required
def inventory(shop_id):
    """Shop inventory management"""
    shop = Shop.query.get_or_404(shop_id)
    
    # Check if user owns this shop
    if shop.owner_id != current_user.id:
        flash('You do not have permission to access this shop', 'error')
        return redirect(url_for('main.index'))
    
    products = Product.query.filter_by(shop_id=shop_id).all()
    
    return render_template('shop/inventory.html', shop=shop, products=products)


@shop_bp.route('/<int:shop_id>/add-product', methods=['POST'])
@login_required
def add_product(shop_id):
    """
    Add product to shop inventory.
    
    Creates a new product entry for the specified shop.
    Validates shop ownership and form data.
    
    Args:
        shop_id (int): ID of the shop to add product to
        
    Returns:
        JSON: Success response with product ID or error message
    """
    try:
        shop = Shop.query.get(shop_id)
        if not shop:
            return jsonify({'error': 'Shop not found'}), 404
        
        # Check if user owns this shop
        if shop.owner_id != current_user.id:
            return handle_permission_error("You do not have permission to add products to this shop")
        product = Product(
            name=request.form.get('name'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            price=request.form.get('price', type=float),
            unit=request.form.get('unit'),
            quantity_available=request.form.get('quantity_available', type=int),
            min_order_quantity=request.form.get('min_order_quantity', type=int),
            shop_id=shop_id
        )
        
        db.session.add(product)
        db.session.commit()
        
        return jsonify({'success': True, 'product_id': product.id})
    except Exception as e:
        return handle_api_error(e)


@shop_bp.route('/<int:shop_id>/orders')
@login_required
def shop_orders(shop_id):
    """Shop orders management"""
    shop = Shop.query.get_or_404(shop_id)
    
    # Check if user owns this shop
    if shop.owner_id != current_user.id:
        flash('You do not have permission to access this shop', 'error')
        return redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(shop_id=shop_id)\
                       .order_by(Order.created_at.desc())\
                       .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('shop/orders.html', shop=shop, orders=orders)
