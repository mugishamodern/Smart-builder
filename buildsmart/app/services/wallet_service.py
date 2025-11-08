"""
Wallet service for user wallet and transaction management.

This module provides functionality for managing user wallets,
including credits, debits, and transaction history.
"""
import secrets
from datetime import datetime
from decimal import Decimal
from app.extensions import db
from app.models import Wallet, Transaction, User


class WalletService:
    """Service for wallet management"""
    
    @staticmethod
    def get_or_create_wallet(user_id):
        """
        Get or create wallet for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Wallet: User's wallet
        """
        wallet = Wallet.query.filter_by(user_id=user_id).first()
        
        if not wallet:
            wallet = Wallet(
                user_id=user_id,
                balance=Decimal('0.00'),
                currency='NGN'
            )
            db.session.add(wallet)
            db.session.commit()
        
        return wallet
    
    @staticmethod
    def generate_transaction_reference():
        """Generate unique transaction reference."""
        return f"TXN-{secrets.token_hex(6).upper()}"
    
    @staticmethod
    def credit_wallet(user_id, amount, description=None, related_type=None, related_id=None):
        """
        Credit wallet with amount.
        
        Args:
            user_id: User ID
            amount: Amount to credit
            description: Transaction description
            related_type: Type of related entity
            related_id: ID of related entity
            
        Returns:
            Transaction: Created transaction
        """
        wallet = WalletService.get_or_create_wallet(user_id)
        
        transaction = wallet.credit(
            amount=amount,
            description=description or 'Wallet credit'
        )
        
        if transaction:
            transaction.reference = WalletService.generate_transaction_reference()
            transaction.related_type = related_type
            transaction.related_id = related_id
            db.session.commit()
        
        return transaction
    
    @staticmethod
    def debit_wallet(user_id, amount, description=None, related_type=None, related_id=None):
        """
        Debit wallet with amount.
        
        Args:
            user_id: User ID
            amount: Amount to debit
            description: Transaction description
            related_type: Type of related entity
            related_id: ID of related entity
            
        Returns:
            Transaction: Created transaction or None if insufficient balance
        """
        wallet = WalletService.get_or_create_wallet(user_id)
        
        if not wallet.has_sufficient_balance(amount):
            return None
        
        transaction = wallet.debit(
            amount=amount,
            description=description or 'Wallet debit'
        )
        
        if transaction:
            transaction.reference = WalletService.generate_transaction_reference()
            transaction.related_type = related_type
            transaction.related_id = related_id
            db.session.commit()
        
        return transaction
    
    @staticmethod
    def get_wallet_balance(user_id):
        """
        Get wallet balance for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            Decimal: Wallet balance
        """
        wallet = WalletService.get_or_create_wallet(user_id)
        return wallet.balance
    
    @staticmethod
    def get_transactions(user_id, transaction_type=None, limit=None, page=None):
        """
        Get transactions for a user.
        
        Args:
            user_id: User ID
            transaction_type: Filter by type (credit, debit)
            limit: Maximum number of transactions
            page: Page number for pagination
            
        Returns:
            list or pagination: List of transactions
        """
        wallet = WalletService.get_or_create_wallet(user_id)
        
        query = Transaction.query.filter_by(wallet_id=wallet.id)
        
        if transaction_type:
            query = query.filter_by(transaction_type=transaction_type)
        
        query = query.order_by(Transaction.created_at.desc())
        
        if page:
            return query.paginate(page=page, per_page=limit or 20, error_out=False)
        
        if limit:
            query = query.limit(limit)
        
        return query.all()
    
    @staticmethod
    def transfer_between_wallets(from_user_id, to_user_id, amount, description=None):
        """
        Transfer funds between wallets.
        
        Args:
            from_user_id: Source user ID
            to_user_id: Destination user ID
            amount: Amount to transfer
            description: Transaction description
            
        Returns:
            tuple: (success, error_message, transactions)
        """
        # Debit from source wallet
        debit_transaction = WalletService.debit_wallet(
            from_user_id,
            amount,
            description=f"Transfer to user {to_user_id}: {description or ''}",
            related_type='transfer',
            related_id=to_user_id
        )
        
        if not debit_transaction:
            return False, 'Insufficient balance', None
        
        # Credit to destination wallet
        credit_transaction = WalletService.credit_wallet(
            to_user_id,
            amount,
            description=f"Transfer from user {from_user_id}: {description or ''}",
            related_type='transfer',
            related_id=from_user_id
        )
        
        return True, None, (debit_transaction, credit_transaction)
    
    @staticmethod
    def get_wallet_summary(user_id):
        """
        Get wallet summary for a user.
        
        Args:
            user_id: User ID
            
        Returns:
            dict: Wallet summary
        """
        wallet = WalletService.get_or_create_wallet(user_id)
        
        # Get recent transactions
        recent_transactions = WalletService.get_transactions(user_id, limit=10)
        
        # Calculate totals
        total_credits = db.session.query(db.func.sum(Transaction.amount)).filter_by(
            wallet_id=wallet.id,
            transaction_type='credit',
            status='completed'
        ).scalar() or Decimal('0.00')
        
        total_debits = db.session.query(db.func.sum(Transaction.amount)).filter_by(
            wallet_id=wallet.id,
            transaction_type='debit',
            status='completed'
        ).scalar() or Decimal('0.00')
        
        return {
            'wallet_id': wallet.id,
            'balance': float(wallet.balance),
            'currency': wallet.currency,
            'total_credits': float(total_credits),
            'total_debits': float(total_debits),
            'recent_transactions': [{
                'id': t.id,
                'type': t.transaction_type,
                'amount': float(t.amount),
                'description': t.description,
                'status': t.status,
                'created_at': t.created_at.isoformat()
            } for t in recent_transactions]
        }

