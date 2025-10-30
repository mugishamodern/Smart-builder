from datetime import datetime
from app.extensions import db
import math


class Shop(db.Model):
    """
    Shop model for construction material shops.
    
    This model represents physical and online shops that sell
    construction materials and building supplies. It includes
    location data for proximity-based searches and rating systems.
    
    Attributes:
        id (int): Primary key
        name (str): Shop name
        description (str): Shop description
        address (str): Physical address
        phone (str): Contact phone number
        email (str): Contact email
        latitude (float): GPS latitude for location services
        longitude (float): GPS longitude for location services
        rating (float): Average customer rating (0.0-5.0)
        total_reviews (int): Total number of reviews
        is_verified (bool): Whether shop is verified by platform
        is_active (bool): Whether shop is currently active
        created_at (datetime): Shop registration timestamp
        updated_at (datetime): Last update timestamp
        owner_id (int): Foreign key to User (shop owner)
    
    Relationships:
        products: One-to-many relationship with Product model
        orders: One-to-many relationship with Order model
        owner: Many-to-one relationship with User model
    """
    __tablename__ = 'shops'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    address = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    rating = db.Column(db.Float, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)
    is_verified = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    products = db.relationship('Product', backref='shop', lazy=True)
    orders = db.relationship('Order', backref='shop', lazy=True)
    
    def distance_to(self, lat, lon):
        """
        Calculate distance to given coordinates in kilometers.
        
        Uses the Haversine formula to calculate the great-circle distance
        between two points on Earth given their latitude and longitude.
        
        Args:
            lat (float): Target latitude in decimal degrees
            lon (float): Target longitude in decimal degrees
            
        Returns:
            float: Distance in kilometers
        """
        # Haversine formula
        R = 6371  # Earth's radius in kilometers
        
        lat1_rad = math.radians(self.latitude)
        lat2_rad = math.radians(lat)
        delta_lat = math.radians(lat - self.latitude)
        delta_lon = math.radians(lon - self.longitude)
        
        a = (math.sin(delta_lat / 2) ** 2 + 
             math.cos(lat1_rad) * math.cos(lat2_rad) * 
             math.sin(delta_lon / 2) ** 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c
    
    def total_products_count(self):
        """
        Get total number of products in this shop.
        
        Returns:
            int: Total number of products associated with this shop
        """
        return len(self.products)
    
    def __str__(self):
        return f"{self.name} - {self.address}"
    
    def __repr__(self):
        return f'<Shop {self.name}>'
