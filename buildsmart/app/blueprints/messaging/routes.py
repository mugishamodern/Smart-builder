"""
Messaging routes for the messaging blueprint.

Provides REST API endpoints for:
- Sending messages
- Fetching conversations
- Getting conversation messages
- Marking messages as read
- Getting unread message count
- Admin: View all conversations
"""
from flask import render_template, request, jsonify
from flask_login import login_required, current_user
from app.blueprints.messaging import messaging_bp
from app.models import Message, Conversation, User, MessageAttachment
from app.extensions import db, socketio
from app.services.attachment_service import AttachmentService
from app.utils.decorators import admin_required
from app.utils.error_handlers import (
    handle_api_error, handle_validation_error, handle_permission_error,
    handle_not_found_error, validate_required_fields, validate_json_request
)
from sqlalchemy import or_, and_


@messaging_bp.route('/messages')
@login_required
def inbox():
    """Display user's message inbox"""
    conversations = Conversation.query.filter(
        or_(
            Conversation.participant_1_id == current_user.id,
            Conversation.participant_2_id == current_user.id
        )
    ).order_by(Conversation.last_message_at.desc()).all()
    
    return render_template('messaging/inbox.html', conversations=conversations)


@messaging_bp.route('/messages/<int:user_id>')
@login_required
def chat(user_id):
    """Display chat interface with specific user"""
    other_user = User.query.get_or_404(user_id)
    
    # Get or create conversation
    conversation = Conversation.query.filter(
        or_(
            and_(Conversation.participant_1_id == current_user.id, 
                 Conversation.participant_2_id == user_id),
            and_(Conversation.participant_1_id == user_id, 
                 Conversation.participant_2_id == current_user.id)
        )
    ).first()
    
    # Get messages
    messages = Message.query.filter(
        or_(
            and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
            and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
        )
    ).order_by(Message.timestamp.asc()).all()
    
    return render_template('messaging/chat.html', 
                         other_user=other_user, 
                         conversation=conversation,
                         messages=messages)


# ============================================================
# API Endpoints
# ============================================================

@messaging_bp.route('/api/messages/send', methods=['POST'])
@login_required
def api_send_message():
    """Send a message via API"""
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        is_valid, field_errors = validate_required_fields(data, ['receiver_id', 'content'])
        if not is_valid:
            return handle_validation_error(field_errors)
        
        receiver_id = data.get('receiver_id')
        content = data.get('content', '').strip()
        
        if not content:
            return handle_validation_error({'content': 'Message content cannot be empty'})
        
        # Verify receiver exists
        receiver = User.query.get(receiver_id)
        if not receiver:
            return handle_not_found_error("User")
        
        if receiver_id == current_user.id:
            return handle_validation_error({'receiver_id': 'Cannot send message to yourself'})
        
        # Create message
        message = Message(
            sender_id=current_user.id,
            receiver_id=receiver_id,
            content=content,
            is_read=False
        )
        db.session.add(message)
        
        # Update or create conversation
        conversation = Conversation.query.filter(
            or_(
                and_(Conversation.participant_1_id == current_user.id, 
                     Conversation.participant_2_id == receiver_id),
                and_(Conversation.participant_1_id == receiver_id, 
                     Conversation.participant_2_id == current_user.id)
            )
        ).first()
        
        from datetime import datetime
        if not conversation:
            # Create new conversation (smaller ID first)
            if current_user.id < receiver_id:
                conversation = Conversation(
                    participant_1_id=current_user.id,
                    participant_2_id=receiver_id,
                    last_message_at=datetime.utcnow(),
                    last_message_preview=content[:100],
                    unread_count_2=1
                )
            else:
                conversation = Conversation(
                    participant_1_id=receiver_id,
                    participant_2_id=current_user.id,
                    last_message_at=datetime.utcnow(),
                    last_message_preview=content[:100],
                    unread_count_1=1
                )
            db.session.add(conversation)
        else:
            conversation.last_message_at = datetime.utcnow()
            conversation.last_message_preview = content[:100]
            # Increment unread count for receiver
            if conversation.participant_1_id == receiver_id:
                conversation.unread_count_1 += 1
            else:
                conversation.unread_count_2 += 1
        
        db.session.commit()
        
        # Handle file attachments if present
        attachments_data = []
        if 'attachments' in request.files:
            files = request.files.getlist('attachments')
            for file in files:
                if file and file.filename:
                    attachment = AttachmentService.save_attachment(file, message.id)
                    if attachment:
                        attachments_data.append(attachment.to_dict())
        
        # Emit SocketIO event for real-time updates
        message_dict = message.to_dict()
        message_dict['attachments'] = attachments_data
        socketio.emit('new_message', message_dict, room=f"user_{receiver_id}")
        socketio.emit('new_message', message_dict, room=f"user_{current_user.id}")  # Also send to sender so they see their message
        
        return jsonify({
            'success': True,
            'message': message_dict,
            'attachments': attachments_data
        }), 201
    
    except Exception as e:
        return handle_api_error(e)


@messaging_bp.route('/api/messages/conversations', methods=['GET'])
@login_required
def api_get_conversations():
    """Get all conversations for current user"""
    try:
        conversations = Conversation.query.filter(
            or_(
                Conversation.participant_1_id == current_user.id,
                Conversation.participant_2_id == current_user.id
            )
        ).order_by(Conversation.last_message_at.desc()).all()
        
        return jsonify({
            'success': True,
            'conversations': [conv.to_dict(current_user.id) for conv in conversations]
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


@messaging_bp.route('/api/messages/conversation/<int:user_id>', methods=['GET'])
@login_required
def api_get_conversation(user_id):
    """Get conversation messages with specific user"""
    try:
        other_user = User.query.get(user_id)
        if not other_user:
            return handle_not_found_error("User")
        
        # Get messages
        messages = Message.query.filter(
            or_(
                and_(Message.sender_id == current_user.id, Message.receiver_id == user_id),
                and_(Message.sender_id == user_id, Message.receiver_id == current_user.id)
            )
        ).order_by(Message.timestamp.asc()).all()
        
        # Get attachments for each message
        messages_data = []
        for msg in messages:
            msg_dict = msg.to_dict()
            attachments = AttachmentService.get_message_attachments(msg.id)
            msg_dict['attachments'] = [att.to_dict() for att in attachments]
            messages_data.append(msg_dict)
        
        return jsonify({
            'success': True,
            'messages': messages_data,
            'other_user': {
                'id': other_user.id,
                'username': other_user.username,
                'full_name': other_user.full_name,
                'user_type': other_user.user_type
            }
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


@messaging_bp.route('/api/messages/<int:message_id>/read', methods=['PUT'])
@login_required
def api_mark_message_read(message_id):
    """Mark a message as read"""
    try:
        message = Message.query.get(message_id)
        if not message:
            return handle_not_found_error("Message")
        
        if message.receiver_id != current_user.id:
            return handle_permission_error("You can only mark messages sent to you as read")
        
        if not message.is_read:
            message.is_read = True
            
            # Update conversation unread count
            conversation = Conversation.query.filter(
                or_(
                    and_(Conversation.participant_1_id == current_user.id, 
                         Conversation.participant_2_id == message.sender_id),
                    and_(Conversation.participant_1_id == message.sender_id, 
                         Conversation.participant_2_id == current_user.id)
                )
            ).first()
            
            if conversation:
                if conversation.participant_1_id == current_user.id:
                    conversation.unread_count_1 = max(0, conversation.unread_count_1 - 1)
                else:
                    conversation.unread_count_2 = max(0, conversation.unread_count_2 - 1)
            
            db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Message marked as read'
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


@messaging_bp.route('/api/messages/conversation/<int:user_id>/read', methods=['PUT'])
@login_required
def api_mark_conversation_read(user_id):
    """Mark all messages in a conversation as read"""
    try:
        # Mark all messages from sender as read
        messages = Message.query.filter_by(
            sender_id=user_id,
            receiver_id=current_user.id,
            is_read=False
        ).all()
        
        for msg in messages:
            msg.is_read = True
        
        # Update conversation unread count
        conversation = Conversation.query.filter(
            or_(
                and_(Conversation.participant_1_id == current_user.id, 
                     Conversation.participant_2_id == user_id),
                and_(Conversation.participant_1_id == user_id, 
                     Conversation.participant_2_id == current_user.id)
            )
        ).first()
        
        if conversation:
            if conversation.participant_1_id == current_user.id:
                conversation.unread_count_1 = 0
            else:
                conversation.unread_count_2 = 0
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Conversation marked as read'
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


@messaging_bp.route('/api/messages/unread-count', methods=['GET'])
@login_required
def api_get_unread_count():
    """Get total unread message count for current user"""
    try:
        unread_count = Message.query.filter_by(
            receiver_id=current_user.id,
            is_read=False
        ).count()
        
        return jsonify({
            'success': True,
            'unread_count': unread_count
        }), 200
    
    except Exception as e:
        return handle_api_error(e)


# ============================================================
# Admin Routes
# ============================================================

@messaging_bp.route('/admin/messages')
@login_required
@admin_required
def admin_messages():
    """Admin dashboard to view all conversations"""
    conversations = Conversation.query.order_by(
        Conversation.last_message_at.desc()
    ).all()
    
    return render_template('admin/messages.html', conversations=conversations)


@messaging_bp.route('/api/admin/users/search', methods=['GET'])
@login_required
@admin_required
def api_admin_search_users():
    """Search users for admin to initiate conversations"""
    try:
        query = request.args.get('q', '').strip()
        
        if len(query) < 2:
            return jsonify({
                'success': True,
                'users': []
            }), 200
        
        # Search users by username, email, or full_name
        users = User.query.filter(
            or_(
                User.username.ilike(f'%{query}%'),
                User.email.ilike(f'%{query}%'),
                User.full_name.ilike(f'%{query}%')
            )
        ).limit(10).all()
        
        return jsonify({
            'success': True,
            'users': [{
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'user_type': user.user_type
            } for user in users]
        }), 200
    
    except Exception as e:
        return handle_api_error(e)
