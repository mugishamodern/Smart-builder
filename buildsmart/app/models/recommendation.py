from datetime import datetime
from app.extensions import db


class Recommendation(db.Model):
    """
    Recommendation model for AI-generated project recommendations.
    
    This model stores AI-generated recommendations for construction
    projects, including cost estimates and material suggestions.
    
    Attributes:
        id (int): Primary key
        project_type (str): Type of project (e.g., '2_bedroom_house', 'office_building')
        project_description (str): Detailed project description
        total_estimated_cost (Decimal): Total estimated project cost
        recommendation_data (JSON): Full recommendation data as JSON
        is_saved (bool): Whether recommendation is saved by user
        created_at (datetime): Recommendation creation timestamp
        updated_at (datetime): Last update timestamp
        user_id (int): Foreign key to User
    
    Relationships:
        user: Many-to-one relationship with User model
    """
    __tablename__ = 'recommendations'
    
    id = db.Column(db.Integer, primary_key=True)
    project_type = db.Column(db.String(50), nullable=False)  # e.g., '2_bedroom_house', 'office_building'
    project_description = db.Column(db.Text, nullable=False)
    total_estimated_cost = db.Column(db.Numeric(12, 2))
    recommendation_data = db.Column(db.JSON, nullable=False)  # Store the full recommendation as JSON
    is_saved = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    def __str__(self):
        return f"Recommendation for {self.project_type} - ${self.total_estimated_cost or 'TBD'}"
    
    def __repr__(self):
        return f'<Recommendation {self.id}>'
