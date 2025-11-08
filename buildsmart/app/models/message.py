from datetime import datetime
from app.extensions import db


class Message(db.Model):
    """
    Message model for real-time messaging between users.
    
    This model represents individual messages in conversations between
    users, shops, and admin. Supports read/unread status tracking.
    
    Attributes:
        id (int): Primary key
        sender_id (int): Foreign key to User (message sender)
        receiver_id (int): Foreign key to User (message receiver)
        content (str): Message content/text
        timestamp (datetime): Message creation timestamp
        is_read (bool): Whether message has been read by receiver
    
    Relationships:
        sender: Many-to-one relationship with User model (sender)
        receiver: Many-to-one relationship with User model (receiver)
    """
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    is_read = db.Column(db.Boolean, default=False, nullable=False)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    receiver = db.relationship('User', foreign_keys=[receiver_id], backref='received_messages')
    
    def to_dict(self):
        """Convert message to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'sender_id': self.sender_id,
            'receiver_id': self.receiver_id,
            'sender_name': self.sender.full_name or self.sender.username if self.sender else None,
            'receiver_name': self.receiver.full_name or self.receiver.username if self.receiver else None,
            'content': self.content,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'is_read': self.is_read
        }
    
    def __repr__(self):
        return f'<Message {self.id} from {self.sender_id} to {self.receiver_id}>'


class Conversation(db.Model):
    """
    Conversation model for tracking message threads between users.
    
    This model represents conversation threads, making it easier to
    query and display conversations in a messaging interface.
    
    Attributes:
        id (int): Primary key
        participant_1_id (int): Foreign key to User (first participant)
        participant_2_id (int): Foreign key to User (second participant)
        last_message_at (datetime): Timestamp of most recent message
        last_message_preview (str): Preview of last message content
        unread_count_1 (int): Unread count for participant 1
        unread_count_2 (int): Unread count for participant 2
    
    Relationships:
        participant_1: Many-to-one relationship with User model
        participant_2: Many-to-one relationship with User model
    """
    __tablename__ = 'conversations'
    
    id = db.Column(db.Integer, primary_key=True)
    participant_1_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    participant_2_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    last_message_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_message_preview = db.Column(db.Text)
    unread_count_1 = db.Column(db.Integer, default=0)  # Unread for participant_1
    unread_count_2 = db.Column(db.Integer, default=0)  # Unread for participant_2
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    participant_1 = db.relationship('User', foreign_keys=[participant_1_id], backref='conversations_as_p1')
    participant_2 = db.relationship('User', foreign_keys=[participant_2_id], backref='conversations_as_p2')
    
    def get_other_participant(self, user_id):
        """Get the other participant in this conversation"""
        if self.participant_1_id == user_id:
            return self.participant_2
        return self.participant_1
    
    def get_unread_count(self, user_id):
        """Get unread message count for a specific user"""
        if self.participant_1_id == user_id:
            return self.unread_count_1
        return self.unread_count_2
    
    def to_dict(self, current_user_id):
        """Convert conversation to dictionary for JSON serialization"""
        other_participant = self.get_other_participant(current_user_id)
        return {
            'id': self.id,
            'other_participant': {
                'id': other_participant.id,
                'username': other_participant.username,
                'full_name': other_participant.full_name,
                'user_type': other_participant.user_type
            },
            'last_message_at': self.last_message_at.isoformat() if self.last_message_at else None,
            'last_message_preview': self.last_message_preview,
            'unread_count': self.get_unread_count(current_user_id)
        }
    
    def __repr__(self):
        return f'<Conversation {self.id} between {self.participant_1_id} and {self.participant_2_id}>'
