"""
SocketIO event handlers for real-time messaging.

This module handles WebSocket events for the messaging system,
including connection management, message sending, and read status updates.
"""
from flask import request
from flask_login import current_user
from app.extensions import socketio, db
from app.models import Message, Conversation, User
from datetime import datetime


@socketio.on('connect')
def handle_connect(auth):
    """
    Handle client connection to SocketIO.
    
    Args:
        auth: Authentication data (optional, can contain user_id or token)
    """
    # In a real implementation, verify the user is authenticated
    # For now, we'll use session-based auth from Flask-Login
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        # Join a room for the user to receive messages
        socketio.server.enter_room(request.sid, f"user_{current_user.id}")
        print(f"User {current_user.id} ({current_user.username}) connected to SocketIO")
        return True
    else:
        print("Unauthenticated connection attempt")
        return False


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection from SocketIO."""
    if hasattr(current_user, 'is_authenticated') and current_user.is_authenticated:
        print(f"User {current_user.id} ({current_user.username}) disconnected from SocketIO")
        socketio.server.leave_room(request.sid, f"user_{current_user.id}")


@socketio.on('send_message')
def handle_send_message(data):
    """
    Handle incoming message from client.
    
    Args:
        data: Dictionary containing:
            - receiver_id: ID of message receiver
            - content: Message content/text
    
    Emits:
        - new_message: To receiver's room
        - message_sent: Confirmation to sender
    """
    if not (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated):
        socketio.emit('error', {'message': 'Authentication required'}, room=request.sid)
        return
    
    receiver_id = data.get('receiver_id')
    content = data.get('content', '').strip()
    
    if not receiver_id or not content:
        socketio.emit('error', {'message': 'Invalid message data'}, room=request.sid)
        return
    
    # Verify receiver exists
    receiver = User.query.get(receiver_id)
    if not receiver:
        socketio.emit('error', {'message': 'Receiver not found'}, room=request.sid)
        return
    
    # Create message in database
    message = Message(
        sender_id=current_user.id,
        receiver_id=receiver_id,
        content=content,
        is_read=False
    )
    db.session.add(message)
    
    # Update or create conversation
    conversation = Conversation.query.filter(
        ((Conversation.participant_1_id == current_user.id) & 
         (Conversation.participant_2_id == receiver_id)) |
        ((Conversation.participant_1_id == receiver_id) & 
         (Conversation.participant_2_id == current_user.id))
    ).first()
    
    if not conversation:
        # Create new conversation (always store smaller ID first for consistency)
        if current_user.id < receiver_id:
            conversation = Conversation(
                participant_1_id=current_user.id,
                participant_2_id=receiver_id,
                last_message_at=datetime.utcnow(),
                last_message_preview=content[:100],
                unread_count_2=1  # Receiver has 1 unread
            )
        else:
            conversation = Conversation(
                participant_1_id=receiver_id,
                participant_2_id=current_user.id,
                last_message_at=datetime.utcnow(),
                last_message_preview=content[:100],
                unread_count_1=1  # Receiver (participant_1) has 1 unread
            )
        db.session.add(conversation)
    else:
        # Update existing conversation
        conversation.last_message_at = datetime.utcnow()
        conversation.last_message_preview = content[:100]
        # Increment unread count for receiver
        if conversation.participant_1_id == receiver_id:
            conversation.unread_count_1 += 1
        else:
            conversation.unread_count_2 += 1
    
    db.session.commit()
    
    # Emit to receiver if online
    message_dict = message.to_dict()
    socketio.emit('new_message', message_dict, room=f"user_{receiver_id}")
    
    # Send confirmation to sender
    socketio.emit('message_sent', {
        'message_id': message.id,
        'receiver_id': receiver_id,
        'timestamp': message.timestamp.isoformat()
    }, room=request.sid)


@socketio.on('mark_as_read')
def handle_mark_as_read(data):
    """
    Handle marking messages as read.
    
    Args:
        data: Dictionary containing:
            - message_id: ID of message to mark as read (optional)
            - conversation_id: ID of conversation to mark all as read (optional)
            - sender_id: ID of sender to mark all messages from them as read (optional)
    """
    if not (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated):
        socketio.emit('error', {'message': 'Authentication required'}, room=request.sid)
        return
    
    message_id = data.get('message_id')
    conversation_id = data.get('conversation_id')
    sender_id = data.get('sender_id')
    
    if message_id:
        # Mark single message as read
        message = Message.query.filter_by(
            id=message_id,
            receiver_id=current_user.id
        ).first()
        if message and not message.is_read:
            message.is_read = True
            db.session.commit()
    
    elif sender_id:
        # Mark all messages from sender as read
        messages = Message.query.filter_by(
            sender_id=sender_id,
            receiver_id=current_user.id,
            is_read=False
        ).all()
        for msg in messages:
            msg.is_read = True
        
        # Update conversation unread count
        conversation = Conversation.query.filter(
            ((Conversation.participant_1_id == current_user.id) & 
             (Conversation.participant_2_id == sender_id)) |
            ((Conversation.participant_1_id == sender_id) & 
             (Conversation.participant_2_id == current_user.id))
        ).first()
        if conversation:
            if conversation.participant_1_id == current_user.id:
                conversation.unread_count_1 = 0
            else:
                conversation.unread_count_2 = 0
            db.session.commit()
    
    elif conversation_id:
        # Mark all messages in conversation as read
        conversation = Conversation.query.get(conversation_id)
        if conversation and (
            conversation.participant_1_id == current_user.id or
            conversation.participant_2_id == current_user.id
        ):
            other_user_id = conversation.participant_1_id if conversation.participant_2_id == current_user.id else conversation.participant_2_id
            messages = Message.query.filter_by(
                sender_id=other_user_id,
                receiver_id=current_user.id,
                is_read=False
            ).all()
            for msg in messages:
                msg.is_read = True
            
            # Update conversation unread count
            if conversation.participant_1_id == current_user.id:
                conversation.unread_count_1 = 0
            else:
                conversation.unread_count_2 = 0
            db.session.commit()
    
    socketio.emit('messages_read', {'status': 'success'}, room=request.sid)


@socketio.on('join_conversation')
def handle_join_conversation(data):
    """
    Handle joining a conversation room for real-time updates.
    
    Args:
        data: Dictionary containing:
            - user_id: Current user ID
            - other_user_id: Other participant's ID
    """
    if not (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated):
        return
    
    other_user_id = data.get('other_user_id')
    if other_user_id:
        # Join a conversation-specific room
        room_name = f"conversation_{min(current_user.id, other_user_id)}_{max(current_user.id, other_user_id)}"
        socketio.server.enter_room(request.sid, room_name)


@socketio.on('typing')
def handle_typing(data):
    """
    Handle typing indicator.
    
    Args:
        data: Dictionary containing:
            - receiver_id or other_user_id: ID of receiver to notify
            - is_typing: Boolean indicating if user is typing (optional)
    """
    if not (hasattr(current_user, 'is_authenticated') and current_user.is_authenticated):
        return
    
    receiver_id = data.get('receiver_id') or data.get('other_user_id')
    
    if receiver_id:
        socketio.emit('user_typing', {
            'user_id': current_user.id,
            'sender_name': current_user.full_name or current_user.username,
            'is_typing': True
        }, room=f"user_{receiver_id}")
