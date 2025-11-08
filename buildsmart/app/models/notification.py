"""
In-app notification model for user notifications.

This module provides a model for in-app notifications
that are separate from messages, including order updates,
system notifications, and other alerts.
"""
from datetime import datetime
from app.extensions import db


class Notification(db.Model):
    """
    In-app notification model for user notifications.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        notification_type (str): Type of notification
        title (str): Notification title
        message (str): Notification message/content
        link (str): Optional link/URL
        related_id (int): Related entity ID (order, product, etc.)
        related_type (str): Type of related entity
        is_read (bool): Whether notification has been read
        read_at (datetime): When notification was read
        created_at (datetime): When notification was created
        priority (str): Priority level (low, normal, high, urgent)
    """
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # order, system, promotion, alert, etc.
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    link = db.Column(db.String(500), nullable=True)
    related_id = db.Column(db.Integer, nullable=True)  # ID of related entity
    related_type = db.Column(db.String(50), nullable=True)  # order, product, shop, etc.
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    read_at = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), default='normal')  # low, normal, high, urgent
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    user = db.relationship('User', backref='notifications', lazy=True)
    
    def mark_as_read(self):
        """Mark notification as read."""
        self.is_read = True
        self.read_at = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convert notification to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'notification_type': self.notification_type,
            'title': self.title,
            'message': self.message,
            'link': self.link,
            'related_id': self.related_id,
            'related_type': self.related_type,
            'is_read': self.is_read,
            'read_at': self.read_at.isoformat() if self.read_at else None,
            'priority': self.priority,
            'created_at': self.created_at.isoformat()
        }
    
    def __repr__(self):
        return f'<Notification {self.id} type={self.notification_type} user_id={self.user_id}>'


class NotificationPreference(db.Model):
    """
    Notification preference model for user notification settings.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User
        notification_type (str): Type of notification
        email_enabled (bool): Whether email notifications are enabled
        sms_enabled (bool): Whether SMS notifications are enabled
        push_enabled (bool): Whether push notifications are enabled
        in_app_enabled (bool): Whether in-app notifications are enabled
    """
    __tablename__ = 'notification_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # order, system, promotion, etc.
    email_enabled = db.Column(db.Boolean, default=True, nullable=False)
    sms_enabled = db.Column(db.Boolean, default=False, nullable=False)
    push_enabled = db.Column(db.Boolean, default=True, nullable=False)
    in_app_enabled = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='notification_preferences', lazy=True)
    
    # Unique constraint: one preference per user per notification type
    __table_args__ = (db.UniqueConstraint('user_id', 'notification_type', name='unique_user_notification_preference'),)
    
    def __repr__(self):
        return f'<NotificationPreference user_id={self.user_id} type={self.notification_type}>'

