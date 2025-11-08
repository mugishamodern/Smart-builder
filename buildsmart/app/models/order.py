from datetime import datetime
from app.extensions import db


class Order(db.Model):
    """
    Order model for customer orders.
    
    This model represents customer orders for products from shops,
    including order status, payment information, and delivery details.
    
    Attributes:
        id (int): Primary key
        order_number (str): Unique order number
        status (str): Order status (pending, confirmed, processing, shipped, delivered, cancelled)
        total_amount (Decimal): Total order amount
        delivery_address (str): Delivery address
        delivery_notes (str): Special delivery instructions
        payment_status (str): Payment status (pending, paid, failed, refunded)
        payment_method (str): Payment method used
        created_at (datetime): Order creation timestamp
        updated_at (datetime): Last update timestamp
        customer_id (int): Foreign key to User (customer)
        shop_id (int): Foreign key to Shop
    
    Relationships:
        items: One-to-many relationship with OrderItem model
        customer: Many-to-one relationship with User model
        shop: Many-to-one relationship with Shop model
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal_amount = db.Column(db.Numeric(10, 2), nullable=True)  # Amount before tax and discount
    discount_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    tax_amount = db.Column(db.Numeric(10, 2), default=0.00, nullable=False)
    coupon_code = db.Column(db.String(50), nullable=True)  # Applied coupon code
    delivery_address = db.Column(db.Text)
    delivery_notes = db.Column(db.Text)
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, failed, refunded
    payment_method = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    customer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    shop_id = db.Column(db.Integer, db.ForeignKey('shops.id'), nullable=False)
    
    # Relationships
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def add_status_history(self, status, notes=None, created_by=None):
        """
        Add status history entry for this order.
        
        Args:
            status: Order status
            notes: Optional notes
            created_by: User ID who changed status
        """
        from app.models import OrderStatus
        status_entry = OrderStatus(
            order_id=self.id,
            status=status,
            notes=notes,
            created_by=created_by
        )
        db.session.add(status_entry)
        db.session.commit()
    
    def __str__(self):
        return f"Order {self.order_number} - {self.status} (${self.total_amount})"
    
    def __repr__(self):
        return f'<Order {self.order_number}>'


class OrderItem(db.Model):
    """
    Order item model for individual products in an order.
    
    This model represents individual line items within an order,
    storing quantity, pricing, and product information.
    
    Attributes:
        id (int): Primary key
        quantity (int): Quantity ordered
        unit_price (Decimal): Price per unit at time of order
        total_price (Decimal): Total price for this line item
        order_id (int): Foreign key to Order
        product_id (int): Foreign key to Product
    
    Relationships:
        order: Many-to-one relationship with Order model
        product: Many-to-one relationship with Product model
    """
    __tablename__ = 'order_items'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    
    # Foreign keys
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    
    def __str__(self):
        return f"{self.product.name} x{self.quantity} = ${self.total_price}"
    
    def __repr__(self):
        return f'<OrderItem {self.id}>'
