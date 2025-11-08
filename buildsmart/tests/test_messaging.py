"""
Tests for messaging system (Message and Conversation models).
"""
import pytest
from app.extensions import db
from app.models import User, Message, Conversation
from app.extensions import bcrypt


def test_create_message(db, auth_client):
    """Test creating a message."""
    client, sender = auth_client
    
    # Create a receiver
    receiver = User(
        username='receiver',
        email='receiver@example.com',
        password_hash=bcrypt.generate_password_hash('pass123').decode('utf-8'),
        full_name='Receiver User',
        user_type='customer'
    )
    db.session.add(receiver)
    db.session.commit()
    
    # Send message via API
    response = client.post('/api/messages/send', json={
        'receiver_id': receiver.id,
        'content': 'Test message'
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify message in database
    message = Message.query.filter_by(
        sender_id=sender.id,
        receiver_id=receiver.id
    ).first()
    assert message is not None
    assert message.content == 'Test message'
    assert message.is_read is False


def test_get_conversations(db, auth_client):
    """Test getting user's conversations."""
    client, user1 = auth_client
    
    # Create another user
    user2 = User(
        username='user2',
        email='user2@example.com',
        password_hash=bcrypt.generate_password_hash('pass123').decode('utf-8'),
        full_name='User 2',
        user_type='customer'
    )
    db.session.add(user2)
    db.session.commit()
    
    # Create a conversation
    conversation = Conversation(
        participant_1_id=user1.id,
        participant_2_id=user2.id,
        last_message_preview='Hello'
    )
    db.session.add(conversation)
    
    # Create a message
    message = Message(
        sender_id=user1.id,
        receiver_id=user2.id,
        content='Hello',
        conversation_id=conversation.id
    )
    db.session.add(message)
    db.session.commit()
    
    # Get conversations via API
    response = client.get('/api/messages/conversations')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['conversations']) > 0


def test_mark_message_as_read(db, auth_client):
    """Test marking a message as read."""
    client, user1 = auth_client
    
    # Create another user
    user2 = User(
        username='user2',
        email='user2@example.com',
        password_hash=bcrypt.generate_password_hash('pass123').decode('utf-8'),
        full_name='User 2',
        user_type='customer'
    )
    db.session.add(user2)
    db.session.commit()
    
    # Create a message
    message = Message(
        sender_id=user2.id,
        receiver_id=user1.id,
        content='Test message',
        is_read=False
    )
    db.session.add(message)
    db.session.commit()
    
    # Mark as read via API
    response = client.put(f'/api/messages/{message.id}/read')
    
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    
    # Verify message is marked as read
    db.session.refresh(message)
    assert message.is_read is True
