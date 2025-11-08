"""
Attachment service for message file attachments.

This module provides functionality for handling file uploads
for message attachments, including PDFs, images, and documents.
"""
import os
import uuid
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from flask import current_app
from app.extensions import db
from app.models import MessageAttachment, Message


class AttachmentService:
    """Service for handling message attachments"""
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {
        'pdf': 'application/pdf',
        'jpg': 'image/jpeg',
        'jpeg': 'image/jpeg',
        'png': 'image/png',
        'gif': 'image/gif',
        'doc': 'application/msword',
        'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'xls': 'application/vnd.ms-excel',
        'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'txt': 'text/plain'
    }
    
    # Maximum file size (10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024
    
    @staticmethod
    def allowed_file(filename):
        """
        Check if file extension is allowed.
        
        Args:
            filename: File name
            
        Returns:
            bool: True if allowed, False otherwise
        """
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in AttachmentService.ALLOWED_EXTENSIONS
    
    @staticmethod
    def get_file_type(filename):
        """
        Get MIME type for file.
        
        Args:
            filename: File name
            
        Returns:
            str: MIME type or None
        """
        ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        return AttachmentService.ALLOWED_EXTENSIONS.get(ext)
    
    @staticmethod
    def validate_file(file):
        """
        Validate attachment file.
        
        Args:
            file: FileStorage object
            
        Returns:
            tuple: (is_valid, error_message)
        """
        if not file:
            return False, 'No file provided'
        
        if file.filename == '':
            return False, 'No file selected'
        
        if not AttachmentService.allowed_file(file.filename):
            allowed = ', '.join(AttachmentService.ALLOWED_EXTENSIONS.keys())
            return False, f'Invalid file type. Allowed types: {allowed}'
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > AttachmentService.MAX_FILE_SIZE:
            return False, f'File too large. Maximum size: {AttachmentService.MAX_FILE_SIZE / (1024 * 1024)}MB'
        
        return True, None
    
    @staticmethod
    def save_attachment(file, message_id):
        """
        Save attachment file.
        
        Args:
            file: FileStorage object
            message_id: Message ID
            
        Returns:
            MessageAttachment: Created attachment or None
        """
        # Validate file
        is_valid, error_msg = AttachmentService.validate_file(file)
        if not is_valid:
            current_app.logger.error(f'Attachment validation failed: {error_msg}')
            return None
        
        try:
            # Generate unique filename
            filename = secure_filename(file.filename)
            ext = filename.rsplit('.', 1)[1].lower()
            unique_filename = f"{uuid.uuid4().hex}.{ext}"
            
            # Create directory
            upload_folder = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'uploads'),
                'attachments'
            )
            os.makedirs(upload_folder, exist_ok=True)
            
            # Save file
            file_path = os.path.join(upload_folder, unique_filename)
            file.save(file_path)
            
            # Get file size
            file_size = os.path.getsize(file_path)
            
            # Get file type
            file_type = AttachmentService.get_file_type(filename)
            
            # Generate URL (relative to static folder)
            file_url = f"/uploads/attachments/{unique_filename}"
            
            # Create attachment record
            attachment = MessageAttachment(
                message_id=message_id,
                file_name=filename,
                file_path=file_url,
                file_type=file_type,
                file_size=file_size
            )
            
            db.session.add(attachment)
            db.session.commit()
            
            return attachment
            
        except Exception as e:
            current_app.logger.error(f'Error saving attachment: {str(e)}')
            db.session.rollback()
            return None
    
    @staticmethod
    def delete_attachment(attachment_id):
        """
        Delete attachment and its file.
        
        Args:
            attachment_id: Attachment ID
            
        Returns:
            bool: True if deleted successfully, False otherwise
        """
        try:
            attachment = MessageAttachment.query.get(attachment_id)
            if not attachment:
                return False
            
            # Delete file
            upload_folder = os.path.join(
                current_app.config.get('UPLOAD_FOLDER', 'uploads'),
                'attachments'
            )
            file_path = os.path.join(upload_folder, attachment.file_path.split('/')[-1])
            
            if os.path.exists(file_path):
                os.remove(file_path)
            
            # Delete database record
            db.session.delete(attachment)
            db.session.commit()
            
            return True
            
        except Exception as e:
            current_app.logger.error(f'Error deleting attachment: {str(e)}')
            db.session.rollback()
            return False
    
    @staticmethod
    def get_message_attachments(message_id):
        """
        Get all attachments for a message.
        
        Args:
            message_id: Message ID
            
        Returns:
            list: List of attachments
        """
        return MessageAttachment.query.filter_by(message_id=message_id).all()

