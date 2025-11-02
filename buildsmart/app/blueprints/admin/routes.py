from flask import render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.blueprints.admin import admin_bp
from app.models import User, Shop, Product, Order, Payment, Category, Review
from app.extensions import db
from app.services.payment_service import payment_service
from app.utils.decorators import admin_required
from datetime import datetime, timedelta


@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """
    Admin dashboard with overview statistics.
    
    Returns:
        str: Rendered dashboard template
    """
    # Calculate statistics
    total_shops = Shop.query.count()
    total_clients = User.query.filter(User.user_type == 'customer').count()
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    pending_shops = Shop.query.filter_by(is_verified=False, is_active=True).count()
    pending_payments = Payment.query.filter_by(status=Payment.STATUS_HELD_BY_ADMIN).count()
    
    # Recent orders (last 10)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Recent shop registrations
    recent_shops = Shop.query.order_by(Shop.created_at.desc()).limit(5).all()
    
    # Pending verifications
    pending_verifications = Shop.query.filter_by(is_verified=False, is_active=True).all()
    
    stats = {
        'total_shops': total_shops,
        'total_clients': total_clients,
        'total_sales': float(total_sales),
        'pending_shops': pending_shops,
        'pending_payments': pending_payments
    }
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         recent_shops=recent_shops,
                         pending_verifications=pending_verifications)


@admin_bp.route('/shops')
@login_required
@admin_required
def shops():
    """
    List all shops with filtering options.
    
    Returns:
        str: Rendered shops list template
    """
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')  # all, verified, pending, rejected
    
    query = Shop.query
    
    if status_filter == 'verified':
        query = query.filter_by(is_verified=True)
    elif status_filter == 'pending':
        query = query.filter_by(is_verified=False, is_active=True)
    elif status_filter == 'rejected':
        query = query.filter_by(is_active=False)
    
    shops = query.order_by(Shop.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/shops.html', shops=shops, status_filter=status_filter)


@admin_bp.route('/shops/<int:shop_id>')
@login_required
@admin_required
def shop_detail(shop_id):
    """
    View detailed information about a specific shop.
    
    Args:
        shop_id: Shop ID
    
    Returns:
        str: Rendered shop detail template
    """
    shop = Shop.query.get_or_404(shop_id)
    products = Product.query.filter_by(shop_id=shop_id).all()
    orders = Order.query.filter_by(shop_id=shop_id).order_by(Order.created_at.desc()).limit(10).all()
    
    # Calculate shop statistics
    total_orders = Order.query.filter_by(shop_id=shop_id).count()
    total_revenue = db.session.query(db.func.sum(Order.total_amount)).filter_by(shop_id=shop_id).scalar() or 0
    
    shop_stats = {
        'total_products': len(products),
        'total_orders': total_orders,
        'total_revenue': float(total_revenue)
    }
    
    return render_template('admin/shop_detail.html',
                         shop=shop,
                         products=products,
                         orders=orders,
                         shop_stats=shop_stats)


@admin_bp.route('/shops/<int:shop_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_shop(shop_id):
    """
    Verify/approve a shop registration.
    
    Args:
        shop_id: Shop ID
    
    Returns:
        JSON: Success or error response
    """
    shop = Shop.query.get_or_404(shop_id)
    
    notes = request.form.get('notes', '')
    
    shop.is_verified = True
    shop.verified_at = datetime.utcnow()
    shop.verified_by = current_user.id
    shop.verification_notes = notes
    
    db.session.commit()
    
    flash('Shop verified successfully!', 'success')
    return redirect(url_for('admin.shops'))


@admin_bp.route('/shops/<int:shop_id>/reject', methods=['POST'])
@login_required
@admin_required
def reject_shop(shop_id):
    """
    Reject a shop registration.
    
    Args:
        shop_id: Shop ID
    
    Returns:
        JSON: Success or error response
    """
    shop = Shop.query.get_or_404(shop_id)
    
    notes = request.form.get('notes', '')
    
    if not notes:
        flash('Please provide a reason for rejection.', 'error')
        return redirect(url_for('admin.shop_detail', shop_id=shop_id))
    
    shop.is_active = False
    shop.verification_notes = notes
    
    db.session.commit()
    
    flash('Shop registration rejected.', 'success')
    return redirect(url_for('admin.shops'))


@admin_bp.route('/payments')
@login_required
@admin_required
def payments():
    """
    List all payments with filtering options.
    
    Returns:
        str: Rendered payments list template
    """
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')  # all, pending, held, released, refunded
    
    query = Payment.query
    
    if status_filter == 'pending':
        query = query.filter_by(status=Payment.STATUS_PENDING_ADMIN)
    elif status_filter == 'held':
        query = query.filter_by(status=Payment.STATUS_HELD_BY_ADMIN)
    elif status_filter == 'released':
        query = query.filter_by(status=Payment.STATUS_RELEASED_TO_SHOP)
    elif status_filter == 'refunded':
        query = query.filter_by(status=Payment.STATUS_REFUNDED)
    
    payments = query.order_by(Payment.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/payments.html', payments=payments, status_filter=status_filter)


@admin_bp.route('/payments/<int:payment_id>/release', methods=['POST'])
@login_required
@admin_required
def release_payment(payment_id):
    """
    Release payment from escrow to shop.
    
    Args:
        payment_id: Payment ID
    
    Returns:
        JSON: Success or error response
    """
    notes = request.form.get('notes', '')
    
    try:
        payment_service.release_to_shop(payment_id, current_user.id, notes)
        flash('Payment released successfully!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('admin.payments'))


@admin_bp.route('/payments/<int:payment_id>/refund', methods=['POST'])
@login_required
@admin_required
def refund_payment(payment_id):
    """
    Refund payment to customer.
    
    Args:
        payment_id: Payment ID
    
    Returns:
        JSON: Success or error response
    """
    reason = request.form.get('reason', '')
    
    if not reason:
        flash('Please provide a reason for refund.', 'error')
        return redirect(url_for('admin.payments'))
    
    try:
        payment_service.refund_to_customer(payment_id, reason)
        flash('Payment refunded successfully!', 'success')
    except ValueError as e:
        flash(str(e), 'error')
    
    return redirect(url_for('admin.payments'))


@admin_bp.route('/analytics')
@login_required
@admin_required
def analytics():
    """
    Analytics dashboard with charts and statistics.
    
    Returns:
        str: Rendered analytics template
    """
    # Sales trends (last 30 days)
    thirty_days_ago = datetime.utcnow() - timedelta(days=30)
    recent_orders = Order.query.filter(Order.created_at >= thirty_days_ago).all()
    
    # Popular products
    from app.models import OrderItem
    popular_products = db.session.query(
        Product.name,
        db.func.sum(OrderItem.quantity).label('total_quantity')
    ).join(OrderItem).group_by(Product.id, Product.name).order_by(
        db.func.sum(OrderItem.quantity).desc()
    ).limit(10).all()
    
    # Top shops
    top_shops = db.session.query(
        Shop.name,
        db.func.sum(Order.total_amount).label('total_revenue'),
        db.func.count(Order.id).label('total_orders')
    ).join(Order).group_by(Shop.id, Shop.name).order_by(
        db.func.sum(Order.total_amount).desc()
    ).limit(10).all()
    
    # Category distribution
    category_dist = db.session.query(
        Product.category,
        db.func.count(Product.id).label('product_count')
    ).group_by(Product.category).all()
    
    # Calculate sales by day for chart
    sales_by_day = {}
    for order in recent_orders:
        day = order.created_at.date()
        if day not in sales_by_day:
            sales_by_day[day] = 0
        sales_by_day[day] += float(order.total_amount)
    
    return render_template('admin/analytics.html',
                         popular_products=popular_products,
                         top_shops=top_shops,
                         category_dist=category_dist,
                         sales_by_day=sales_by_day)


@admin_bp.route('/users')
@login_required
@admin_required
def users():
    """
    List all users with filtering options.
    
    Returns:
        str: Rendered users list template
    """
    page = request.args.get('page', 1, type=int)
    user_type_filter = request.args.get('user_type', 'all')
    
    query = User.query
    
    if user_type_filter != 'all':
        query = query.filter_by(user_type=user_type_filter)
    
    users = query.order_by(User.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/users.html', users=users, user_type_filter=user_type_filter)


@admin_bp.route('/users/<int:user_id>/verify', methods=['POST'])
@login_required
@admin_required
def verify_user(user_id):
    """
    Verify a user account.
    
    Args:
        user_id: User ID
    
    Returns:
        redirect: Redirect to users list
    """
    user = User.query.get_or_404(user_id)
    user.is_verified = True
    db.session.commit()
    
    flash('User verified successfully!', 'success')
    return redirect(url_for('admin.users'))


@admin_bp.route('/users/<int:user_id>/suspend', methods=['POST'])
@login_required
@admin_required
def suspend_user(user_id):
    """
    Suspend a user account.
    
    Args:
        user_id: User ID
    
    Returns:
        redirect: Redirect to users list
    """
    user = User.query.get_or_404(user_id)
    user.is_active = False
    db.session.commit()
    
    flash('User suspended successfully!', 'success')
    return redirect(url_for('admin.users'))

