"""
Message attachment model for file attachments in messages.

This module provides a model for storing file attachments
in messages, supporting PDFs, images, and documents.
"""
from datetime import datetime
from app.extensions import db


class MessageAttachment(db.Model):
    """
    Message attachment model for file attachments.
    
    Attributes:
        id (int): Primary key
        message_id (int): Foreign key to Message
        file_name (str): Original file name
        file_path (str): Path to stored file
        file_type (str): File MIME type
        file_size (int): File size in bytes
        uploaded_at (datetime): When file was uploaded
    """
    __tablename__ = 'message_attachments'
    
    id = db.Column(db.Integer, primary_key=True)
    message_id = db.Column(db.Integer, db.ForeignKey('messages.id'), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_type = db.Column(db.String(100), nullable=False)  # MIME type
    file_size = db.Column(db.Integer, nullable=False)  # Size in bytes
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationship
    message = db.relationship('Message', backref='attachments', lazy=True)
    
    def to_dict(self):
        """Convert attachment to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'message_id': self.message_id,
            'file_name': self.file_name,
            'file_path': self.file_path,
            'file_type': self.file_type,
            'file_size': self.file_size,
            'uploaded_at': self.uploaded_at.isoformat()
        }
    
    def __repr__(self):
        return f'<MessageAttachment {self.id} file={self.file_name}>'

