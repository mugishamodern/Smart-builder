"""
Dispute resolution service.

This module provides functionality for managing disputes
between customers and shop owners/service providers.
"""
import secrets
from datetime import datetime
from app.extensions import db
from app.models import Dispute, DisputeMessage, Order, Service, User


class DisputeService:
    """Service for dispute resolution"""
    
    @staticmethod
    def generate_dispute_number():
        """Generate unique dispute number."""
        return f"DISP-{secrets.token_hex(4).upper()}"
    
    @staticmethod
    def create_dispute(dispute_type, order_id=None, service_id=None, title, description, raised_by, against):
        """
        Create a new dispute.
        
        Args:
            dispute_type: Type of dispute (order, service, payment, delivery)
            order_id: Order ID (if order-related)
            service_id: Service ID (if service-related)
            title: Dispute title
            description: Detailed description
            raised_by: User ID who raised dispute
            against: User ID who dispute is against
            
        Returns:
            Dispute: Created dispute or None
        """
        # Validate inputs
        if dispute_type == 'order' and not order_id:
            return None
        if dispute_type == 'service' and not service_id:
            return None
        
        # Verify users exist
        raiser = User.query.get(raised_by)
        opponent = User.query.get(against)
        
        if not raiser or not opponent:
            return None
        
        # Generate dispute number
        dispute_number = DisputeService.generate_dispute_number()
        
        # Create dispute
        dispute = Dispute(
            dispute_number=dispute_number,
            dispute_type=dispute_type,
            order_id=order_id,
            service_id=service_id,
            title=title,
            description=description,
            raised_by=raised_by,
            against=against,
            status='open',
            priority='medium'
        )
        
        db.session.add(dispute)
        db.session.commit()
        
        return dispute
    
    @staticmethod
    def add_message(dispute_id, sender_id, message, attachments=None):
        """
        Add a message to a dispute.
        
        Args:
            dispute_id: Dispute ID
            sender_id: User ID who sent message
            message: Message content
            attachments: List of attachment paths/URLs (optional)
            
        Returns:
            DisputeMessage: Created message or None
        """
        dispute = Dispute.query.get(dispute_id)
        if not dispute:
            return None
        
        dispute_message = DisputeMessage(
            dispute_id=dispute_id,
            sender_id=sender_id,
            message=message,
            attachments=attachments or []
        )
        
        db.session.add(dispute_message)
        
        # Update dispute status if needed
        if dispute.status == 'open':
            dispute.status = 'in_review'
        
        dispute.updated_at = datetime.utcnow()
        db.session.commit()
        
        return dispute_message
    
    @staticmethod
    def assign_dispute(dispute_id, user_id):
        """
        Assign dispute to a user (admin).
        
        Args:
            dispute_id: Dispute ID
            user_id: User ID to assign to
            
        Returns:
            bool: True if successful, False otherwise
        """
        dispute = Dispute.query.get(dispute_id)
        if not dispute:
            return False
        
        dispute.assign(user_id)
        
        return True
    
    @staticmethod
    def resolve_dispute(dispute_id, resolver_id, resolution):
        """
        Resolve a dispute.
        
        Args:
            dispute_id: Dispute ID
            resolver_id: User ID who resolved
            resolution: Resolution description
            
        Returns:
            bool: True if successful, False otherwise
        """
        dispute = Dispute.query.get(dispute_id)
        if not dispute:
            return False
        
        dispute.resolve(resolver_id, resolution)
        
        return True
    
    @staticmethod
    def close_dispute(dispute_id):
        """
        Close a dispute.
        
        Args:
            dispute_id: Dispute ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        dispute = Dispute.query.get(dispute_id)
        if not dispute:
            return False
        
        dispute.close()
        
        return True
    
    @staticmethod
    def escalate_dispute(dispute_id):
        """
        Escalate a dispute.
        
        Args:
            dispute_id: Dispute ID
            
        Returns:
            bool: True if successful, False otherwise
        """
        dispute = Dispute.query.get(dispute_id)
        if not dispute:
            return False
        
        dispute.escalate()
        
        return True
    
    @staticmethod
    def get_user_disputes(user_id, status=None):
        """
        Get disputes for a user (as raiser or opponent).
        
        Args:
            user_id: User ID
            status: Filter by status (optional)
            
        Returns:
            list: List of disputes
        """
        query = db.session.query(Dispute).filter(
            (Dispute.raised_by == user_id) | (Dispute.against == user_id)
        )
        
        if status:
            query = query.filter(Dispute.status == status)
        
        return query.order_by(Dispute.created_at.desc()).all()
    
    @staticmethod
    def get_all_disputes(status=None, priority=None):
        """
        Get all disputes (for admins).
        
        Args:
            status: Filter by status (optional)
            priority: Filter by priority (optional)
            
        Returns:
            list: List of disputes
        """
        query = Dispute.query
        
        if status:
            query = query.filter_by(status=status)
        
        if priority:
            query = query.filter_by(priority=priority)
        
        return query.order_by(Dispute.created_at.desc()).all()

