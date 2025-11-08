"""
Search History model for tracking user searches.

This module provides models for tracking user search history,
search suggestions, and trending searches.
"""
from datetime import datetime
from app.extensions import db


class SearchHistory(db.Model):
    """
    Search History model for tracking user searches.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User (nullable for anonymous users)
        query (str): Search query string
        search_type (str): Type of search (products, shops, services)
        results_count (int): Number of results found
        created_at (datetime): When search was performed
    """
    __tablename__ = 'search_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    query = db.Column(db.String(255), nullable=False)
    search_type = db.Column(db.String(50), default='products')  # products, shops, services
    results_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='search_history', lazy=True)
    
    def __repr__(self):
        return f'<SearchHistory query="{self.query}" user_id={self.user_id}>'


class TrendingSearch(db.Model):
    """
    Trending Search model for tracking popular searches.
    
    Attributes:
        id (int): Primary key
        query (str): Search query string
        search_type (str): Type of search
        count (int): Number of times searched
        last_searched (datetime): Last time this query was searched
        created_at (datetime): When trending search was first tracked
    """
    __tablename__ = 'trending_searches'
    
    id = db.Column(db.Integer, primary_key=True)
    query = db.Column(db.String(255), nullable=False, unique=True, index=True)
    search_type = db.Column(db.String(50), default='products')
    count = db.Column(db.Integer, default=1)
    last_searched = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    def increment(self):
        """Increment search count and update last_searched."""
        self.count += 1
        self.last_searched = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<TrendingSearch query="{self.query}" count={self.count}>'

