"""
Analytics models for tracking and reporting metrics.

This module contains models for storing analytics data and metrics.
"""
from datetime import datetime
from app.extensions import db


class AnalyticsMetric(db.Model):
    """
    Model for storing analytics metrics.
    
    This model stores pre-calculated metrics for faster reporting.
    """
    __tablename__ = 'analytics_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    metric_type = db.Column(db.String(50), nullable=False, index=True)  # sales, orders, users, products, etc.
    metric_name = db.Column(db.String(100), nullable=False)  # daily_sales, monthly_orders, etc.
    metric_value = db.Column(db.Numeric(15, 2), nullable=False)
    metric_date = db.Column(db.Date, nullable=False, index=True)
    
    # Optional filters
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=True, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=True, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # Metadata
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    shop = db.relationship('Shop', backref='analytics_metrics', lazy='select')
    category = db.relationship('Category', backref='analytics_metrics', lazy='select')
    user = db.relationship('User', backref='analytics_metrics', lazy='select')
    
    def __repr__(self):
        return f'<AnalyticsMetric {self.metric_type}:{self.metric_name}={self.metric_value}>'
    
    def to_dict(self):
        """Convert metric to dictionary."""
        return {
            'id': self.id,
            'metric_type': self.metric_type,
            'metric_name': self.metric_name,
            'metric_value': float(self.metric_value),
            'metric_date': self.metric_date.isoformat() if self.metric_date else None,
            'shop_id': self.shop_id,
            'category_id': self.category_id,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class ReportSchedule(db.Model):
    """
    Model for scheduled reports.
    
    This model stores scheduled report configurations for automated report generation.
    """
    __tablename__ = 'report_schedules'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    report_type = db.Column(db.String(50), nullable=False)  # sales, orders, inventory, etc.
    schedule_type = db.Column(db.String(20), nullable=False)  # daily, weekly, monthly
    schedule_day = db.Column(db.Integer, nullable=True)  # Day of week/month for weekly/monthly
    schedule_time = db.Column(db.Time, nullable=False)  # Time to generate report
    
    # Filters
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=True)
    date_range_days = db.Column(db.Integer, default=30)  # Number of days to include
    
    # Recipients
    recipient_emails = db.Column(db.Text, nullable=False)  # Comma-separated emails
    
    # Configuration
    format = db.Column(db.String(10), default='pdf')  # pdf, excel, csv
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    
    # Metadata
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    last_run_at = db.Column(db.DateTime, nullable=True)
    next_run_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    shop = db.relationship('Shop', backref='report_schedules', lazy='select')
    creator = db.relationship('User', backref='report_schedules', lazy='select')
    
    def __repr__(self):
        return f'<ReportSchedule {self.name} ({self.schedule_type})>'
    
    def to_dict(self):
        """Convert schedule to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'report_type': self.report_type,
            'schedule_type': self.schedule_type,
            'schedule_day': self.schedule_day,
            'schedule_time': self.schedule_time.strftime('%H:%M:%S') if self.schedule_time else None,
            'shop_id': self.shop_id,
            'date_range_days': self.date_range_days,
            'recipient_emails': self.recipient_emails,
            'format': self.format,
            'is_active': self.is_active,
            'created_by': self.created_by,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_run_at': self.last_run_at.isoformat() if self.last_run_at else None,
            'next_run_at': self.next_run_at.isoformat() if self.next_run_at else None
        }

