from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.blueprints.main import main_bp
from app.models import Shop, Product, Service
from app.extensions import db


@main_bp.route('/')
def index():
    """
    Home page displaying featured content.
    
    Shows featured shops, products, and services to provide
    users with a quick overview of available options.
    
    Returns:
        str: Rendered home page template with featured content
    """
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


@main_bp.route('/favicon.ico')
def favicon():
    """Favicon handler"""
    return '', 204  # No content response


@main_bp.route('/search')
def search():
    """
    Search page for products, shops, and services.
    
    Performs text-based search across products, shops, and services
    based on query parameters. Supports category filtering.
    
    Query Parameters:
        q (str): Search query string
        category (str): Optional category filter
        
    Returns:
        str: Rendered search results page
    """
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


@main_bp.route('/projects')
def projects():
    """General construction inspiration/showcase gallery page."""
    # Creative Commons/stock placeholder images with brief captions
    gallery_items = [
        {
            'title': 'Urban High-Rise',
            'image_url': 'https://images.unsplash.com/photo-1494526585095-c41746248156?auto=format&fit=crop&w=1200&q=80',
            'description': 'Structural steel and glass facade with sustainable features.'
        },
        {
            'title': 'Bridge Engineering',
            'image_url': 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
            'description': 'Precision civil works with modular deck segments.'
        },
        {
            'title': 'Residential Villas',
            'image_url': 'https://images.unsplash.com/photo-1600585152220-90363fe7e115?auto=format&fit=crop&w=1200&q=80',
            'description': 'Modern finishes and energy-efficient envelope.'
        },
        {
            'title': 'Industrial Plant',
            'image_url': 'https://images.unsplash.com/photo-1508385082359-f38ae991e8f2?auto=format&fit=crop&w=1200&q=80',
            'description': 'Heavy equipment installation and process piping.'
        },
        {
            'title': 'Airport Terminal',
            'image_url': 'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80',
            'description': 'Complex MEP coordination and tensile roofing.'
        },
        {
            'title': 'Roadworks & Paving',
            'image_url': 'https://images.unsplash.com/photo-1504307651254-35680f356dfd?auto=format&fit=crop&w=1200&q=80',
            'description': 'Asphalt laying and drainage improvements.'
        }
    ]

    return render_template('projects.html', gallery_items=gallery_items)
