from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.blueprints.user import user_bp
from app.models import User, Order, Recommendation, Comparison, Cart, Shop, Address
from app.extensions import db
from app.ai.recommender import generate_full_recommendation


@user_bp.route('/dashboard')
@login_required
def dashboard():
    """User dashboard"""
    # Get user's recent orders
    recent_orders = Order.query.filter_by(customer_id=current_user.id)\
                              .order_by(Order.created_at.desc())\
                              .limit(5).all()
    
    # Get user's saved recommendations
    saved_recommendations = Recommendation.query.filter_by(
        user_id=current_user.id, 
        is_saved=True
    ).order_by(Recommendation.created_at.desc()).limit(5).all()
    
    # Calculate statistics
    total_orders = Order.query.filter_by(customer_id=current_user.id).count()
    total_recommendations = Recommendation.query.filter_by(user_id=current_user.id).count()
    total_spent = db.session.query(db.func.sum(Order.total_amount))\
                           .filter_by(customer_id=current_user.id).scalar() or 0
    
    stats = {
        'total_orders': total_orders,
        'total_recommendations': total_recommendations,
        'total_bookings': 0,  # Placeholder for future service bookings
        'total_spent': float(total_spent)
    }
    
    return render_template('user/dashboard.html', 
                         recent_orders=recent_orders,
                         saved_recommendations=saved_recommendations,
                         stats=stats)


@user_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    """User profile management"""
    if request.method == 'POST':
        # Update user profile
        current_user.full_name = request.form.get('full_name', current_user.full_name)
        current_user.phone = request.form.get('phone', current_user.phone)
        current_user.address = request.form.get('address', current_user.address)
        current_user.latitude = request.form.get('latitude', type=float) or current_user.latitude
        current_user.longitude = request.form.get('longitude', type=float) or current_user.longitude
        
        db.session.commit()
        flash('Profile updated successfully', 'success')
        return redirect(url_for('user.profile'))
    
    return render_template('user/profile.html')


@user_bp.route('/orders')
@login_required
def orders():
    """User's order history with status filtering"""
    from sqlalchemy.orm import joinedload
    
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', '')
    
    # Build query with eager loading of shop relationship
    query = Order.query.options(joinedload(Order.shop)).filter_by(customer_id=current_user.id)
    
    # Apply status filter if provided
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    # Order by creation date (newest first)
    orders = query.order_by(Order.created_at.desc())\
                  .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('user/orders.html', 
                         orders=orders, 
                         status_filter=status_filter)


@user_bp.route('/orders/<int:order_id>')
@login_required
def order_detail(order_id):
    """View detailed order information"""
    from sqlalchemy.orm import joinedload
    from app.models import OrderItem
    
    # Get order with related data
    order = Order.query.options(
        joinedload(Order.shop),
        joinedload(Order.customer),
        joinedload(Order.items).joinedload(OrderItem.product)
    ).filter_by(
        id=order_id,
        customer_id=current_user.id
    ).first_or_404()
    
    return render_template('user/order_detail.html', order=order)


@user_bp.route('/comparisons')
@login_required
def comparisons():
    """Product comparison page"""
    comparisons = Comparison.query.filter_by(user_id=current_user.id).all()
    return render_template('user/comparisons.html', comparisons=comparisons)


@user_bp.route('/saved-carts')
@login_required
def saved_carts():
    """View and manage saved carts"""
    saved_carts = Cart.query.filter_by(
        user_id=current_user.id,
        is_saved=True
    ).order_by(Cart.updated_at.desc()).all()
    
    return render_template('user/saved_carts.html', saved_carts=saved_carts)


@user_bp.route('/addresses')
@login_required
def addresses():
    """View and manage delivery addresses"""
    addresses = Address.query.filter_by(user_id=current_user.id).order_by(
        Address.is_default.desc(), Address.created_at.desc()
    ).all()
    return render_template('user/addresses.html', addresses=addresses)


@user_bp.route('/reviews/new')
@login_required
def new_review():
    """Submit a review for a shop"""
    order_id = request.args.get('order_id', type=int)
    shop_id = request.args.get('shop_id', type=int)
    
    shop = None
    order = None
    
    if order_id:
        order = Order.query.get_or_404(order_id)
        if order.customer_id != current_user.id:
            flash('You can only review shops from your own orders', 'error')
            return redirect(url_for('user.orders'))
        shop = order.shop
    elif shop_id:
        shop = Shop.query.get_or_404(shop_id)
    
    if not shop:
        flash('Shop not found', 'error')
        return redirect(url_for('user.orders'))
    
    return render_template('user/review_form.html', shop=shop, order=order)


@user_bp.route('/recommendations')
@login_required
def recommendations():
    """User's AI recommendations"""
    page = request.args.get('page', 1, type=int)
    recommendations = Recommendation.query.filter_by(user_id=current_user.id)\
                                        .order_by(Recommendation.created_at.desc())\
                                        .paginate(page=page, per_page=10, error_out=False)
    
    return render_template('user/recommendations.html', recommendations=recommendations)


@user_bp.route('/recommendations/<int:recommendation_id>')
@login_required
def recommendation_detail(recommendation_id):
    """View detailed recommendation"""
    recommendation = Recommendation.query.filter_by(
        id=recommendation_id,
        user_id=current_user.id
    ).first_or_404()
    
    return render_template('user/recommendation_detail.html', recommendation=recommendation)


@user_bp.route('/get-recommendation', methods=['POST'])
@login_required
def get_recommendation():
    """Generate AI recommendation"""
    data = request.get_json()
    
    if not data or 'project_description' not in data:
        return jsonify({'error': 'Project description required'}), 400
    
    try:
        recommendation = generate_full_recommendation(
            user_id=current_user.id,
            project_description=data['project_description'],
            project_type=data.get('project_type', '2_bedroom_house'),
            custom_specs=data.get('custom_specs', {}),
            user_lat=current_user.latitude,
            user_lon=current_user.longitude
        )
        
        return jsonify(recommendation)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
