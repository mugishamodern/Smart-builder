from datetime import datetime
from app.extensions import db


class Service(db.Model):
    """Service model for construction services"""
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
    
    def __repr__(self):
        return f'<Service {self.title}>'
