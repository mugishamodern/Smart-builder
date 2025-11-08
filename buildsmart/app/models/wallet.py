"""
Wallet and Transaction model for user wallet management.

This module provides models for managing user wallets
and financial transactions.
"""
from datetime import datetime
from decimal import Decimal
from app.extensions import db


class Wallet(db.Model):
    """
    Wallet model for user wallet management.
    
    Attributes:
        id (int): Primary key
        user_id (int): Foreign key to User (unique)
        balance (Decimal): Current wallet balance
        currency (str): Currency code (e.g., NGN, USD)
        is_active (bool): Whether wallet is active
        created_at (datetime): When wallet was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    balance = db.Column(db.Numeric(10, 2), default=Decimal('0.00'), nullable=False)
    currency = db.Column(db.String(3), default='NGN', nullable=False)  # NGN, USD, etc.
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='wallet', uselist=False, lazy=True)
    
    def credit(self, amount, description=None):
        """
        Credit wallet with amount.
        
        Args:
            amount: Amount to credit
            description: Description of transaction
            
        Returns:
            Transaction: Created transaction
        """
        from app.models import Transaction
        self.balance += Decimal(str(amount))
        self.updated_at = datetime.utcnow()
        
        transaction = Transaction(
            wallet_id=self.id,
            transaction_type='credit',
            amount=Decimal(str(amount)),
            description=description or 'Wallet credit',
            status='completed'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return transaction
    
    def debit(self, amount, description=None):
        """
        Debit wallet with amount.
        
        Args:
            amount: Amount to debit
            description: Description of transaction
            
        Returns:
            Transaction: Created transaction or None if insufficient balance
        """
        from app.models import Transaction
        
        amount_decimal = Decimal(str(amount))
        
        if self.balance < amount_decimal:
            return None
        
        self.balance -= amount_decimal
        self.updated_at = datetime.utcnow()
        
        transaction = Transaction(
            wallet_id=self.id,
            transaction_type='debit',
            amount=amount_decimal,
            description=description or 'Wallet debit',
            status='completed'
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return transaction
    
    def has_sufficient_balance(self, amount):
        """
        Check if wallet has sufficient balance.
        
        Args:
            amount: Required amount
            
        Returns:
            bool: True if sufficient, False otherwise
        """
        return self.balance >= Decimal(str(amount))
    
    def __repr__(self):
        return f'<Wallet user_id={self.user_id} balance={self.balance} {self.currency}>'


class Transaction(db.Model):
    """
    Transaction model for wallet transactions.
    
    Attributes:
        id (int): Primary key
        wallet_id (int): Foreign key to Wallet
        transaction_type (str): Type of transaction (credit, debit)
        amount (Decimal): Transaction amount
        description (str): Transaction description
        reference (str): Transaction reference number
        status (str): Transaction status (pending, completed, failed, cancelled)
        related_type (str): Type of related entity (order, payment, refund, etc.)
        related_id (int): ID of related entity
        created_at (datetime): When transaction was created
        updated_at (datetime): Last update timestamp
    """
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # credit, debit
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.Text, nullable=True)
    reference = db.Column(db.String(100), unique=True, nullable=True, index=True)
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, cancelled
    related_type = db.Column(db.String(50), nullable=True)  # order, payment, refund, etc.
    related_id = db.Column(db.Integer, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    wallet = db.relationship('Wallet', backref='transactions', lazy=True)
    
    def complete(self):
        """Mark transaction as completed."""
        self.status = 'completed'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def fail(self):
        """Mark transaction as failed."""
        self.status = 'failed'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def cancel(self):
        """Mark transaction as cancelled."""
        self.status = 'cancelled'
        self.updated_at = datetime.utcnow()
        db.session.commit()
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type} {self.amount} status={self.status}>'

