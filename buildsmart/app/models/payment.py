from datetime import datetime
from app.extensions import db


class Payment(db.Model):
    """
    Payment model for tracking payments and escrow management.
    
    This model represents payments in the system, tracking
    the escrow flow from customer payment to shop release.
    
    Attributes:
        id (int): Primary key
        order_id (int): Foreign key to Order
        amount (Decimal): Payment amount
        payment_method (str): Payment method used
        status (str): Payment status (pending_admin, held_by_admin, released_to_shop, refunded)
        transaction_id (str): Unique transaction identifier
        paid_at (datetime): When payment was completed
        released_at (datetime): When payment was released to shop
        refunded_at (datetime): When refund was issued
        admin_notes (str): Admin notes or remarks
        created_at (datetime): Payment creation timestamp
        updated_at (datetime): Last update timestamp
    
    Relationships:
        order: Many-to-one relationship with Order model
    """
    __tablename__ = 'payments'
    
    # Status constants
    STATUS_PENDING_ADMIN = 'pending_admin'  # Payment pending admin processing
    STATUS_HELD_BY_ADMIN = 'held_by_admin'  # Payment in escrow
    STATUS_RELEASED_TO_SHOP = 'released_to_shop'  # Payment released to shop
    STATUS_REFUNDED = 'refunded'  # Payment refunded to customer
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)  # mobile_money, bank_transfer, cash
    status = db.Column(db.String(30), default=STATUS_PENDING_ADMIN)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    paid_at = db.Column(db.DateTime, nullable=True)
    released_at = db.Column(db.DateTime, nullable=True)
    refunded_at = db.Column(db.DateTime, nullable=True)
    admin_notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    order = db.relationship('Order', backref='payment', lazy=True)
    
    def is_pending(self):
        """Check if payment is pending"""
        return self.status == self.STATUS_PENDING_ADMIN
    
    def is_held(self):
        """Check if payment is held in escrow"""
        return self.status == self.STATUS_HELD_BY_ADMIN
    
    def is_released(self):
        """Check if payment is released to shop"""
        return self.status == self.STATUS_RELEASED_TO_SHOP
    
    def is_refunded(self):
        """Check if payment is refunded"""
        return self.status == self.STATUS_REFUNDED
    
    def __repr__(self):
        return f'<Payment {self.transaction_id} - {self.status}>'

