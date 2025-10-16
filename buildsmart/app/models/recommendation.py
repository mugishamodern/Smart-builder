from datetime import datetime
from app.extensions import db


class Recommendation(db.Model):
    """Recommendation model for AI-generated recommendations"""
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
    
    def __repr__(self):
        return f'<Recommendation {self.id}>'
