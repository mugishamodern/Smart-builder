"""
Cart utility functions for cart operations.
"""
from app.models import Cart, CartItem
from app.extensions import db


def merge_guest_cart_to_user(user_id, session_id):
    """
    Merge guest cart items into user's cart on login.
    
    Args:
        user_id: The logged-in user's ID
        session_id: Guest session identifier
    """
    try:
        # Get guest cart
        guest_cart = Cart.query.filter_by(session_id=session_id, user_id=None, is_saved=False).first()
        
        if not guest_cart or not guest_cart.items:
            return  # No guest cart to merge
        
        # Get or create user's active cart
        user_cart = Cart.query.filter_by(user_id=user_id, is_saved=False).first()
        if not user_cart:
            user_cart = Cart(user_id=user_id, is_saved=False)
            db.session.add(user_cart)
            db.session.flush()
        
        # Merge items from guest cart
        for guest_item in guest_cart.items:
            # Check if product still exists and is available
            if not guest_item.product or not guest_item.product.is_available:
                continue
            
            # Check if item already in user cart
            existing_item = CartItem.query.filter_by(
                cart_id=user_cart.id,
                product_id=guest_item.product_id
            ).first()
            
            if existing_item:
                # Update quantity (add guest quantity to user cart quantity)
                new_quantity = existing_item.quantity + guest_item.quantity
                # Ensure we don't exceed available stock
                if new_quantity <= guest_item.product.quantity_available:
                    existing_item.quantity = new_quantity
                else:
                    # Set to max available
                    existing_item.quantity = guest_item.product.quantity_available
                # Update price snapshot
                existing_item.price_snapshot = guest_item.product.price
            else:
                # Add new item to user cart
                new_item = CartItem(
                    cart_id=user_cart.id,
                    product_id=guest_item.product_id,
                    quantity=min(guest_item.quantity, guest_item.product.quantity_available),
                    price_snapshot=guest_item.product.price
                )
                db.session.add(new_item)
        
        # Delete guest cart after merging
        db.session.delete(guest_cart)
        db.session.commit()
    except Exception as e:
        # Log error but don't fail login
        print(f"Error merging cart: {e}")
        db.session.rollback()
