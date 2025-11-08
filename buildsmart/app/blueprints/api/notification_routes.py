"""
Notification center API routes.

This module provides endpoints for managing in-app notifications,
including viewing, marking as read, and managing preferences.
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import Notification, NotificationPreference
from app.extensions import db
from app.services.notification_service import NotificationService
from app.utils.error_handlers import (
    handle_api_error, handle_validation_error, validate_json_request
)


@api_bp.route('/notifications', methods=['GET'])
@login_required
def get_notifications():
    """
    Get user's notifications.
    
    Returns:
        JSON response with notifications
    """
    try:
        unread_only = request.args.get('unread_only', 'false').lower() == 'true'
        limit = request.args.get('limit', type=int)
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        
        query = Notification.query.filter_by(user_id=current_user.id)
        
        if unread_only:
            query = query.filter_by(is_read=False)
        
        query = query.order_by(Notification.created_at.desc())
        
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        notifications_data = [notification.to_dict() for notification in pagination.items]
        
        return jsonify({
            'notifications': notifications_data,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'unread_count': NotificationService.get_unread_count(current_user.id)
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notifications/unread-count', methods=['GET'])
@login_required
def get_unread_count():
    """
    Get unread notification count.
    
    Returns:
        JSON response with unread count
    """
    try:
        count = NotificationService.get_unread_count(current_user.id)
        
        return jsonify({
            'unread_count': count
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notifications/<int:notification_id>/read', methods=['POST'])
@login_required
def mark_notification_read(notification_id):
    """
    Mark notification as read.
    
    Args:
        notification_id: Notification ID
        
    Returns:
        JSON response
    """
    try:
        success = NotificationService.mark_as_read(notification_id, current_user.id)
        
        if not success:
            return jsonify({
                'error': 'Notification not found'
            }), 404
        
        return jsonify({
            'message': 'Notification marked as read'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notifications/read-all', methods=['POST'])
@login_required
def mark_all_read():
    """
    Mark all notifications as read.
    
    Returns:
        JSON response
    """
    try:
        count = NotificationService.mark_all_as_read(current_user.id)
        
        return jsonify({
            'message': f'{count} notifications marked as read'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
@login_required
def delete_notification(notification_id):
    """
    Delete a notification.
    
    Args:
        notification_id: Notification ID
        
    Returns:
        JSON response
    """
    try:
        success = NotificationService.delete_notification(notification_id, current_user.id)
        
        if not success:
            return jsonify({
                'error': 'Notification not found'
            }), 404
        
        return jsonify({
            'message': 'Notification deleted'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notification-preferences', methods=['GET'])
@login_required
def get_notification_preferences():
    """
    Get user's notification preferences.
    
    Returns:
        JSON response with preferences
    """
    try:
        preferences = NotificationPreference.query.filter_by(
            user_id=current_user.id
        ).all()
        
        preferences_data = {}
        for pref in preferences:
            preferences_data[pref.notification_type] = {
                'email_enabled': pref.email_enabled,
                'sms_enabled': pref.sms_enabled,
                'push_enabled': pref.push_enabled,
                'in_app_enabled': pref.in_app_enabled
            }
        
        return jsonify({
            'preferences': preferences_data
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notification-preferences', methods=['POST'])
@login_required
def update_notification_preferences():
    """
    Update user's notification preferences.
    
    Returns:
        JSON response
    """
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        preferences = data.get('preferences', {})
        
        for notification_type, settings in preferences.items():
            preference = NotificationPreference.query.filter_by(
                user_id=current_user.id,
                notification_type=notification_type
            ).first()
            
            if not preference:
                preference = NotificationPreference(
                    user_id=current_user.id,
                    notification_type=notification_type
                )
                db.session.add(preference)
            
            # Update settings
            if 'email_enabled' in settings:
                preference.email_enabled = settings['email_enabled']
            if 'sms_enabled' in settings:
                preference.sms_enabled = settings['sms_enabled']
            if 'push_enabled' in settings:
                preference.push_enabled = settings['push_enabled']
            if 'in_app_enabled' in settings:
                preference.in_app_enabled = settings['in_app_enabled']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Notification preferences updated'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/notification-preferences/<notification_type>', methods=['PUT'])
@login_required
def update_notification_preference(notification_type):
    """
    Update preference for a specific notification type.
    
    Args:
        notification_type: Notification type
        
    Returns:
        JSON response
    """
    try:
        is_valid, data = validate_json_request()
        if not is_valid:
            return handle_validation_error({'json': data})
        
        preference = NotificationPreference.query.filter_by(
            user_id=current_user.id,
            notification_type=notification_type
        ).first()
        
        if not preference:
            preference = NotificationPreference(
                user_id=current_user.id,
                notification_type=notification_type
            )
            db.session.add(preference)
        
        # Update settings
        if 'email_enabled' in data:
            preference.email_enabled = data['email_enabled']
        if 'sms_enabled' in data:
            preference.sms_enabled = data['sms_enabled']
        if 'push_enabled' in data:
            preference.push_enabled = data['push_enabled']
        if 'in_app_enabled' in data:
            preference.in_app_enabled = data['in_app_enabled']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Notification preference updated',
            'preference': {
                'notification_type': preference.notification_type,
                'email_enabled': preference.email_enabled,
                'sms_enabled': preference.sms_enabled,
                'push_enabled': preference.push_enabled,
                'in_app_enabled': preference.in_app_enabled
            }
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

