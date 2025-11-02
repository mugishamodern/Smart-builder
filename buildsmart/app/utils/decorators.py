from functools import wraps
from flask import flash, redirect, url_for, abort
from flask_login import current_user


def admin_required(f):
    """
    Decorator to require admin access for a route.
    
    Usage:
        @bp.route('/admin/dashboard')
        @login_required
        @admin_required
        def dashboard():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_admin_user():
            flash('You do not have permission to access this page.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    
    return decorated_function


def shop_owner_required(f):
    """
    Decorator to require shop owner access for a route.
    
    Usage:
        @bp.route('/shop/inventory')
        @login_required
        @shop_owner_required
        def inventory():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_shop_owner():
            flash('You do not have shop owner permissions.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    
    return decorated_function


def verified_shop_required(f):
    """
    Decorator to require verified shop access for a route.
    This should be used after shop_owner_required.
    
    Usage:
        @bp.route('/shop/<shop_id>/manage')
        @login_required
        @shop_owner_required
        @verified_shop_required
        def manage_shop(shop_id):
            shop = Shop.query.get_or_404(shop_id)
            if not shop.is_verified:
                flash('This shop is not verified yet.', 'error')
                abort(403)
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # This decorator is used alongside shop_owner_required
        # so we assume the user is already a shop owner at this point
        # The route handler should check if the specific shop is verified
        return f(*args, **kwargs)
    
    return decorated_function


def customer_required(f):
    """
    Decorator to require customer access for a route.
    
    Usage:
        @bp.route('/user/cart')
        @login_required
        @customer_required
        def view_cart():
            ...
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth.login'))
        
        if not current_user.is_customer():
            flash('This page is only accessible to customers.', 'error')
            abort(403)
        
        return f(*args, **kwargs)
    
    return decorated_function

