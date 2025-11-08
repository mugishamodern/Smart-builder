"""
Analytics service for data aggregation and reporting.

This service provides methods for generating analytics data,
creating reports, and aggregating metrics.
"""
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Dict, List, Optional, Tuple
from sqlalchemy import func, and_, or_
from app.extensions import db
from app.models import (
    Order, OrderItem, Product, Shop, User, Category,
    Payment, Review, AnalyticsMetric, OrderStatus
)


class AnalyticsService:
    """Service for analytics and reporting operations."""
    
    @staticmethod
    def get_sales_overview(start_date: Optional[date] = None, end_date: Optional[date] = None) -> Dict:
        """
        Get sales overview statistics.
        
        Args:
            start_date: Start date for filtering (default: 30 days ago)
            end_date: End date for filtering (default: today)
        
        Returns:
            Dict containing sales statistics
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Total sales
        total_sales_query = db.session.query(func.sum(Order.total_amount)).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        )
        total_sales = total_sales_query.scalar() or Decimal('0.00')
        
        # Total orders
        total_orders = Order.query.filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date
            )
        ).count()
        
        # Completed orders
        completed_orders = Order.query.filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.status == OrderStatus.DELIVERED
            )
        ).count()
        
        # Average order value
        avg_order_value = (total_sales / total_orders) if total_orders > 0 else Decimal('0.00')
        
        # Discounts applied
        total_discounts = db.session.query(func.sum(Order.discount_amount)).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.discount_amount.isnot(None)
            )
        ).scalar() or Decimal('0.00')
        
        # Taxes collected
        total_taxes = db.session.query(func.sum(Order.tax_amount)).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.tax_amount.isnot(None)
            )
        ).scalar() or Decimal('0.00')
        
        return {
            'total_sales': float(total_sales),
            'total_orders': total_orders,
            'completed_orders': completed_orders,
            'pending_orders': total_orders - completed_orders,
            'avg_order_value': float(avg_order_value),
            'total_discounts': float(total_discounts),
            'total_taxes': float(total_taxes),
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    
    @staticmethod
    def get_sales_trends(start_date: Optional[date] = None, end_date: Optional[date] = None, 
                        group_by: str = 'day') -> List[Dict]:
        """
        Get sales trends over time.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
            group_by: Grouping period ('day', 'week', 'month')
        
        Returns:
            List of dictionaries with date and sales data
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Build query based on group_by
        if group_by == 'day':
            date_format = func.date(Order.created_at)
        elif group_by == 'week':
            date_format = func.date_trunc('week', Order.created_at)
        elif group_by == 'month':
            date_format = func.date_trunc('month', Order.created_at)
        else:
            date_format = func.date(Order.created_at)
        
        results = db.session.query(
            date_format.label('period'),
            func.sum(Order.total_amount).label('sales'),
            func.count(Order.id).label('orders')
        ).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(date_format).order_by(date_format).all()
        
        trends = []
        for period, sales, orders in results:
            trends.append({
                'period': period.isoformat() if isinstance(period, date) else str(period),
                'sales': float(sales or 0),
                'orders': orders or 0
            })
        
        return trends
    
    @staticmethod
    def get_top_products(limit: int = 10, start_date: Optional[date] = None, 
                        end_date: Optional[date] = None) -> List[Dict]:
        """
        Get top selling products.
        
        Args:
            limit: Number of products to return
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            List of dictionaries with product sales data
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        results = db.session.query(
            Product.id,
            Product.name,
            Product.shop_id,
            Shop.name.label('shop_name'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.sum(OrderItem.total_price).label('total_revenue'),
            func.count(OrderItem.id).label('order_count')
        ).join(OrderItem, Product.id == OrderItem.product_id).join(
            Order, OrderItem.order_id == Order.id
        ).join(Shop, Product.shop_id == Shop.id).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(Product.id, Product.name, Product.shop_id, Shop.name).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(limit).all()
        
        products = []
        for product_id, product_name, shop_id, shop_name, quantity, revenue, order_count in results:
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'shop_id': shop_id,
                'shop_name': shop_name,
                'total_quantity': int(quantity or 0),
                'total_revenue': float(revenue or 0),
                'order_count': order_count or 0
            })
        
        return products
    
    @staticmethod
    def get_top_shops(limit: int = 10, start_date: Optional[date] = None, 
                     end_date: Optional[date] = None) -> List[Dict]:
        """
        Get top performing shops.
        
        Args:
            limit: Number of shops to return
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            List of dictionaries with shop performance data
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        results = db.session.query(
            Shop.id,
            Shop.name,
            func.sum(Order.total_amount).label('total_revenue'),
            func.count(Order.id).label('total_orders'),
            func.avg(Order.total_amount).label('avg_order_value'),
            func.count(func.distinct(Order.customer_id)).label('unique_customers')
        ).join(Order, Shop.id == Order.shop_id).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(Shop.id, Shop.name).order_by(
            func.sum(Order.total_amount).desc()
        ).limit(limit).all()
        
        shops = []
        for shop_id, shop_name, revenue, orders, avg_value, customers in results:
            shops.append({
                'shop_id': shop_id,
                'shop_name': shop_name,
                'total_revenue': float(revenue or 0),
                'total_orders': orders or 0,
                'avg_order_value': float(avg_value or 0),
                'unique_customers': customers or 0
            })
        
        return shops
    
    @staticmethod
    def get_category_performance(start_date: Optional[date] = None, 
                                 end_date: Optional[date] = None) -> List[Dict]:
        """
        Get performance metrics by category.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            List of dictionaries with category performance data
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        results = db.session.query(
            Category.id,
            Category.name,
            func.sum(OrderItem.total_price).label('total_revenue'),
            func.sum(OrderItem.quantity).label('total_quantity'),
            func.count(func.distinct(OrderItem.order_id)).label('order_count'),
            func.count(func.distinct(OrderItem.product_id)).label('product_count')
        ).join(Product, Category.id == Product.category_id).join(
            OrderItem, Product.id == OrderItem.product_id
        ).join(Order, OrderItem.order_id == Order.id).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(Category.id, Category.name).order_by(
            func.sum(OrderItem.total_price).desc()
        ).all()
        
        categories = []
        for cat_id, cat_name, revenue, quantity, orders, products in results:
            categories.append({
                'category_id': cat_id,
                'category_name': cat_name,
                'total_revenue': float(revenue or 0),
                'total_quantity': int(quantity or 0),
                'order_count': orders or 0,
                'product_count': products or 0
            })
        
        return categories
    
    @staticmethod
    def get_user_analytics(start_date: Optional[date] = None, 
                           end_date: Optional[date] = None) -> Dict:
        """
        Get user analytics.
        
        Args:
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            Dictionary with user statistics
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Total users
        total_users = User.query.count()
        
        # New users in period
        new_users = User.query.filter(
            and_(
                func.date(User.created_at) >= start_date,
                func.date(User.created_at) <= end_date
            )
        ).count()
        
        # Active users (users who placed orders)
        active_users = db.session.query(func.count(func.distinct(Order.customer_id))).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date
            )
        ).scalar() or 0
        
        # Users by type
        users_by_type = db.session.query(
            User.user_type,
            func.count(User.id).label('count')
        ).group_by(User.user_type).all()
        
        user_types = {user_type: count for user_type, count in users_by_type}
        
        return {
            'total_users': total_users,
            'new_users': new_users,
            'active_users': active_users,
            'users_by_type': user_types,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    
    @staticmethod
    def get_shop_analytics(shop_id: int, start_date: Optional[date] = None, 
                          end_date: Optional[date] = None) -> Dict:
        """
        Get analytics for a specific shop.
        
        Args:
            shop_id: Shop ID
            start_date: Start date for filtering
            end_date: End date for filtering
        
        Returns:
            Dictionary with shop analytics
        """
        if not start_date:
            start_date = date.today() - timedelta(days=30)
        if not end_date:
            end_date = date.today()
        
        # Shop orders
        orders_query = Order.query.filter_by(shop_id=shop_id).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date
            )
        )
        
        total_orders = orders_query.count()
        total_revenue = db.session.query(func.sum(Order.total_amount)).filter_by(
            shop_id=shop_id
        ).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).scalar() or Decimal('0.00')
        
        # Top products for shop
        top_products = db.session.query(
            Product.id,
            Product.name,
            func.sum(OrderItem.quantity).label('quantity'),
            func.sum(OrderItem.total_price).label('revenue')
        ).join(OrderItem, Product.id == OrderItem.product_id).join(
            Order, OrderItem.order_id == Order.id
        ).filter(
            and_(
                Product.shop_id == shop_id,
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(Product.id, Product.name).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(10).all()
        
        products = []
        for product_id, product_name, quantity, revenue in top_products:
            products.append({
                'product_id': product_id,
                'product_name': product_name,
                'quantity': int(quantity or 0),
                'revenue': float(revenue or 0)
            })
        
        # Sales trends
        trends = db.session.query(
            func.date(Order.created_at).label('date'),
            func.sum(Order.total_amount).label('sales'),
            func.count(Order.id).label('orders')
        ).filter_by(shop_id=shop_id).filter(
            and_(
                func.date(Order.created_at) >= start_date,
                func.date(Order.created_at) <= end_date,
                Order.payment_status == 'paid'
            )
        ).group_by(func.date(Order.created_at)).order_by(
            func.date(Order.created_at)
        ).all()
        
        sales_trends = []
        for order_date, sales, orders in trends:
            sales_trends.append({
                'date': order_date.isoformat(),
                'sales': float(sales or 0),
                'orders': orders or 0
            })
        
        return {
            'shop_id': shop_id,
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'avg_order_value': float(total_revenue / total_orders) if total_orders > 0 else 0.0,
            'top_products': products,
            'sales_trends': sales_trends,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat()
        }
    
    @staticmethod
    def store_metric(metric_type: str, metric_name: str, metric_value: Decimal,
                    metric_date: date, shop_id: Optional[int] = None,
                    category_id: Optional[int] = None, user_id: Optional[int] = None) -> AnalyticsMetric:
        """
        Store a pre-calculated metric.
        
        Args:
            metric_type: Type of metric (sales, orders, users, etc.)
            metric_name: Name of the metric
            metric_value: Value of the metric
            metric_date: Date for the metric
            shop_id: Optional shop filter
            category_id: Optional category filter
            user_id: Optional user filter
        
        Returns:
            Created AnalyticsMetric instance
        """
        metric = AnalyticsMetric(
            metric_type=metric_type,
            metric_name=metric_name,
            metric_value=metric_value,
            metric_date=metric_date,
            shop_id=shop_id,
            category_id=category_id,
            user_id=user_id
        )
        db.session.add(metric)
        db.session.commit()
        return metric

