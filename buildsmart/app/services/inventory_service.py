"""
Inventory management service with low-stock alerts.

This module provides functionality for managing inventory
and generating low-stock alerts for shop owners.
"""
from datetime import datetime
from app.extensions import db
from app.models import Product, InventoryAlert, Shop
from app.services.email_service import EmailService
from flask import current_app


class InventoryService:
    """Service for inventory management"""
    
    @staticmethod
    def check_low_stock(product_id, threshold=None):
        """
        Check if product is low on stock and create alert if needed.
        
        Args:
            product_id: Product ID
            threshold: Low stock threshold (optional, uses product default if not provided)
            
        Returns:
            InventoryAlert: Created alert or None
        """
        product = Product.query.get(product_id)
        if not product:
            return None
        
        # Determine threshold (default to 10 if not set)
        if threshold is None:
            threshold = getattr(product, 'low_stock_threshold', 10)
        
        # Check if low stock
        if product.quantity_available <= threshold and product.quantity_available > 0:
            # Check if alert already exists and is not resolved
            existing_alert = InventoryAlert.query.filter_by(
                product_id=product_id,
                alert_type='low_stock',
                resolved_at=None
            ).first()
            
            if existing_alert:
                # Update existing alert
                existing_alert.current_quantity = product.quantity_available
                existing_alert.threshold = threshold
                db.session.commit()
                return existing_alert
            
            # Create new alert
            alert = InventoryAlert(
                product_id=product_id,
                shop_id=product.shop_id,
                threshold=threshold,
                current_quantity=product.quantity_available,
                alert_type='low_stock'
            )
            db.session.add(alert)
            db.session.commit()
            
            # Send notification to shop owner
            InventoryService.notify_shop_owner(alert)
            
            return alert
        
        # Check if out of stock
        elif product.quantity_available == 0:
            # Check if alert already exists
            existing_alert = InventoryAlert.query.filter_by(
                product_id=product_id,
                alert_type='out_of_stock',
                resolved_at=None
            ).first()
            
            if existing_alert:
                return existing_alert
            
            # Create new alert
            alert = InventoryAlert(
                product_id=product_id,
                shop_id=product.shop_id,
                threshold=0,
                current_quantity=0,
                alert_type='out_of_stock'
            )
            db.session.add(alert)
            db.session.commit()
            
            # Send notification
            InventoryService.notify_shop_owner(alert)
            
            return alert
        
        # Check if restocked (was out of stock, now has stock)
        elif product.quantity_available > 0:
            # Check if there was an out_of_stock alert
            out_of_stock_alert = InventoryAlert.query.filter_by(
                product_id=product_id,
                alert_type='out_of_stock',
                resolved_at=None
            ).first()
            
            if out_of_stock_alert:
                # Resolve old alert
                out_of_stock_alert.resolve()
                
                # Create restocked alert
                alert = InventoryAlert(
                    product_id=product_id,
                    shop_id=product.shop_id,
                    threshold=0,
                    current_quantity=product.quantity_available,
                    alert_type='restocked'
                )
                db.session.add(alert)
                db.session.commit()
                
                return alert
        
        return None
    
    @staticmethod
    def notify_shop_owner(alert):
        """
        Send notification email to shop owner about inventory alert.
        
        Args:
            alert: InventoryAlert object
        """
        try:
            shop = alert.shop
            if not shop or not shop.owner or not shop.owner.email:
                return
            
            product = alert.product
            
            # Prepare email content
            subject = f'Inventory Alert: {product.name}'
            
            if alert.alert_type == 'low_stock':
                message = f'{product.name} is running low. Current stock: {alert.current_quantity} (threshold: {alert.threshold})'
            elif alert.alert_type == 'out_of_stock':
                message = f'{product.name} is out of stock!'
            elif alert.alert_type == 'restocked':
                message = f'{product.name} has been restocked. Current stock: {alert.current_quantity}'
            else:
                message = f'Inventory alert for {product.name}'
            
            # Send email
            from flask import current_app
            frontend_url = current_app.config.get('FRONTEND_URL', 'http://localhost:5000')
            link = f"{frontend_url}/shop/{shop.id}/inventory"
            
            EmailService.send_email(
                subject=subject,
                recipients=[shop.owner.email],
                template='inventory_alert.html',
                user=shop.owner,
                product=product,
                alert=alert,
                message=message,
                link=link
            )
            
            # Mark alert as notified
            alert.mark_as_notified()
            
        except Exception as e:
            current_app.logger.error(f'Error sending inventory alert notification: {str(e)}')
    
    @staticmethod
    def check_all_products(shop_id=None):
        """
        Check all products (or products in a shop) for low stock.
        
        Args:
            shop_id: Shop ID (optional, checks all shops if not provided)
            
        Returns:
            list: List of created alerts
        """
        if shop_id:
            products = Product.query.filter_by(shop_id=shop_id).all()
        else:
            products = Product.query.all()
        
        alerts = []
        for product in products:
            alert = InventoryService.check_low_stock(product.id)
            if alert:
                alerts.append(alert)
        
        return alerts
    
    @staticmethod
    def resolve_alert(alert_id):
        """
        Resolve an inventory alert.
        
        Args:
            alert_id: Alert ID
            
        Returns:
            bool: True if resolved, False otherwise
        """
        alert = InventoryAlert.query.get(alert_id)
        if not alert:
            return False
        
        alert.resolve()
        return True
    
    @staticmethod
    def get_alerts(shop_id, status='active'):
        """
        Get inventory alerts for a shop.
        
        Args:
            shop_id: Shop ID
            status: Alert status ('active' for unresolved, 'all' for all)
            
        Returns:
            list: List of alerts
        """
        query = InventoryAlert.query.filter_by(shop_id=shop_id)
        
        if status == 'active':
            query = query.filter_by(resolved_at=None)
        
        return query.order_by(InventoryAlert.created_at.desc()).all()

