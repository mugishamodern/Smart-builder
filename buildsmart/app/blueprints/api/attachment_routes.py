"""
Message attachment API routes.

This module provides endpoints for managing message attachments,
including upload, download, and deletion.
"""
from flask import jsonify, request, send_file, abort
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import Message, MessageAttachment
from app.extensions import db
from app.services.attachment_service import AttachmentService
from app.utils.error_handlers import handle_api_error, handle_not_found_error, handle_permission_error
import os


@api_bp.route('/messages/<int:message_id>/attachments', methods=['POST'])
@login_required
def upload_message_attachment(message_id):
    """
    Upload attachment for a message.
    
    Args:
        message_id: Message ID
        
    Returns:
        JSON response with attachment details
    """
    try:
        # Check if message exists and user has permission
        message = Message.query.get(message_id)
        if not message:
            return handle_not_found_error("Message")
        
        # Check permissions (sender or receiver)
        if message.sender_id != current_user.id and message.receiver_id != current_user.id:
            return handle_permission_error("You can only add attachments to your own messages")
        
        # Check if files were uploaded
        if 'attachment' not in request.files:
            return jsonify({
                'error': 'Validation error',
                'message': 'No file provided'
            }), 400
        
        file = request.files['attachment']
        
        if not file or file.filename == '':
            return jsonify({
                'error': 'Validation error',
                'message': 'No file selected'
            }), 400
        
        # Validate and save attachment
        is_valid, error_msg = AttachmentService.validate_file(file)
        if not is_valid:
            return jsonify({
                'error': 'Validation error',
                'message': error_msg
            }), 400
        
        attachment = AttachmentService.save_attachment(file, message_id)
        
        if not attachment:
            return jsonify({
                'error': 'Failed to save attachment'
            }), 500
        
        return jsonify({
            'message': 'Attachment uploaded successfully',
            'attachment': attachment.to_dict()
        }), 201
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/messages/<int:message_id>/attachments', methods=['GET'])
@login_required
def get_message_attachments(message_id):
    """
    Get all attachments for a message.
    
    Args:
        message_id: Message ID
        
    Returns:
        JSON response with attachments
    """
    try:
        # Check if message exists and user has permission
        message = Message.query.get(message_id)
        if not message:
            return handle_not_found_error("Message")
        
        # Check permissions (sender or receiver)
        if message.sender_id != current_user.id and message.receiver_id != current_user.id:
            return handle_permission_error("You can only view attachments for your own messages")
        
        attachments = AttachmentService.get_message_attachments(message_id)
        
        attachments_data = [attachment.to_dict() for attachment in attachments]
        
        return jsonify({
            'attachments': attachments_data,
            'count': len(attachments_data)
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/attachments/<int:attachment_id>/download', methods=['GET'])
@login_required
def download_attachment(attachment_id):
    """
    Download an attachment file.
    
    Args:
        attachment_id: Attachment ID
        
    Returns:
        File download response
    """
    try:
        attachment = MessageAttachment.query.get(attachment_id)
        if not attachment:
            return handle_not_found_error("Attachment")
        
        # Check permissions (sender or receiver)
        message = attachment.message
        if message.sender_id != current_user.id and message.receiver_id != current_user.id:
            return handle_permission_error("You can only download attachments from your own messages")
        
        # Get file path
        from flask import current_app
        upload_folder = os.path.join(
            current_app.config.get('UPLOAD_FOLDER', 'uploads'),
            'attachments'
        )
        file_path = os.path.join(upload_folder, attachment.file_path.split('/')[-1])
        
        if not os.path.exists(file_path):
            return handle_not_found_error("File")
        
        return send_file(
            file_path,
            as_attachment=True,
            download_name=attachment.file_name,
            mimetype=attachment.file_type
        )
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/attachments/<int:attachment_id>', methods=['DELETE'])
@login_required
def delete_attachment(attachment_id):
    """
    Delete an attachment.
    
    Args:
        attachment_id: Attachment ID
        
    Returns:
        JSON response
    """
    try:
        attachment = MessageAttachment.query.get(attachment_id)
        if not attachment:
            return handle_not_found_error("Attachment")
        
        # Check permissions (sender only)
        message = attachment.message
        if message.sender_id != current_user.id:
            return handle_permission_error("Only message sender can delete attachments")
        
        success = AttachmentService.delete_attachment(attachment_id)
        
        if not success:
            return jsonify({
                'error': 'Failed to delete attachment'
            }), 500
        
        return jsonify({
            'message': 'Attachment deleted successfully'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

