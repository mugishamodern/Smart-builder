from flask import Flask
from app.extensions import db, migrate, login_manager, bcrypt, cors
from app.config import config
import os


def create_app(config_name=None):
    """Application factory pattern for Flask"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    
    # Configure CORS for API access from mobile/web apps
    # In development, allow all origins for easier testing
    # For credentials to work, we need to explicitly allow the origin
    if config_name == 'development':
        # Simple CORS config for development - allow all origins
        cors.init_app(app, resources={
            r"/api/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Cookie"],
            },
            r"/auth/*": {
                "origins": "*",
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization", "Cookie"],
            },
        }, supports_credentials=True)
    else:
        # In production, configure specific origins
        cors.init_app(app, resources={
            r"/api/*": {
                "origins": ["*"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            },
            r"/auth/*": {
                "origins": ["*"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            },
            r"/user/*": {
                "origins": ["*"],
                "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                "allow_headers": ["Content-Type", "Authorization"],
                "supports_credentials": True,
            }
        })
    
    # Login manager settings
    login_manager.login_view = 'auth.login'
    login_manager.login_message_category = 'info'
    
    # Custom unauthorized handler for API endpoints
    @login_manager.unauthorized_handler
    def unauthorized():
        from flask import request, jsonify
        # For API requests, return JSON error instead of redirect
        if request.path.startswith('/api/'):
            return jsonify({'error': 'Authentication required', 'message': 'Please log in to access this resource'}), 401
        # For web requests, redirect to login (default behavior)
        from flask_login import current_user
        from flask import redirect, url_for, flash
        flash('Please log in to access this page.', 'info')
        return redirect(url_for('auth.login'))
    
    # Import models to register them with SQLAlchemy
    from app.models import User, Shop, Product, Service, Order, OrderItem, Recommendation
    
    # User loader function for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Register blueprints
    from app.blueprints.main import main_bp
    from app.blueprints.auth import auth_bp
    from app.blueprints.user import user_bp
    from app.blueprints.shop import shop_bp
    from app.blueprints.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(shop_bp, url_prefix='/shop')
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app