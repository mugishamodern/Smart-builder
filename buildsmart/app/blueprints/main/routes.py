from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import Shop, Product, Service
from app.extensions import db


@main_bp.route('/')
def index():
    """Home page"""
    # Get featured shops and products
    featured_shops = Shop.query.filter_by(is_verified=True, is_active=True).limit(6).all()
    featured_products = Product.query.filter_by(is_available=True).limit(8).all()
    featured_services = Service.query.filter_by(is_available=True).limit(6).all()
    
    return render_template('home.html', 
                         featured_shops=featured_shops,
                         featured_products=featured_products,
                         featured_services=featured_services)


@main_bp.route('/about')
def about():
    """About page"""
    return render_template('about.html')


@main_bp.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')


@main_bp.route('/search')
def search():
    """Search page"""
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    
    products = []
    shops = []
    services = []
    
    if query:
        # Search products
        products = Product.query.filter(
            (Product.name.ilike(f'%{query}%')) | 
            (Product.description.ilike(f'%{query}%'))
        ).filter_by(is_available=True).limit(20).all()
        
        # Search shops
        shops = Shop.query.filter(
            (Shop.name.ilike(f'%{query}%')) | 
            (Shop.description.ilike(f'%{query}%'))
        ).filter_by(is_active=True).limit(10).all()
        
        # Search services
        services = Service.query.filter(
            (Service.title.ilike(f'%{query}%')) | 
            (Service.description.ilike(f'%{query}%'))
        ).filter_by(is_available=True).limit(10).all()
    
    return render_template('search.html', 
                         query=query,
                         category=category,
                         products=products,
                         shops=shops,
                         services=services)
