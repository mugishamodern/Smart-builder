from datetime import datetime
from app.extensions import db


class Service(db.Model):
    """
    Service model for construction and home improvement services.
    
    This model represents services offered by service providers,
    including pricing, experience, and service area information.
    
    Attributes:
        id (int): Primary key
        title (str): Service title/name
        description (str): Service description
        service_type (str): Type of service (e.g., 'plumbing', 'electrical', 'carpentry')
        hourly_rate (Decimal): Hourly rate for the service
        years_experience (int): Years of experience
        rating (float): Average customer rating (0.0-5.0)
        is_available (bool): Whether service is currently available
        service_area (str): Geographic area served
        certifications (str): Professional certifications
        portfolio_url (str): URL to portfolio or examples
        created_at (datetime): Service creation timestamp
        updated_at (datetime): Last update timestamp
        provider_id (int): Foreign key to User (service provider)
    
    Relationships:
        provider: Many-to-one relationship with User model
    """
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    service_type = db.Column(db.String(50), nullable=False)  # e.g., 'plumbing', 'electrical', 'carpentry'
    hourly_rate = db.Column(db.Numeric(10, 2), nullable=False)
    years_experience = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float, default=0.0)
    is_available = db.Column(db.Boolean, default=True)
    service_area = db.Column(db.String(100))  # e.g., 'Lagos Island', 'Victoria Island'
    certifications = db.Column(db.Text)  # Store certifications as text
    portfolio_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    provider_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __str__(self):
        return f"{self.title} - {self.service_type} (${self.hourly_rate}/hr)"
    
    def __repr__(self):
        return f'<Service {self.title}>'
