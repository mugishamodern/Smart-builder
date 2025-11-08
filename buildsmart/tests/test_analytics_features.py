"""
Tests for Analytics & Reporting features.

This module tests:
- Analytics data aggregation
- Report generation (PDF, Excel)
- Analytics service methods
- Analytics API endpoints
"""
import pytest
from decimal import Decimal
from datetime import datetime, timedelta, date
from flask import current_app
from app.models import (
    User, Order, OrderItem, Product, Shop, Category,
    AnalyticsMetric, ReportSchedule
)
from app.services.analytics_service import AnalyticsService
from app.services.report_service import ReportService
from app.extensions import db


@pytest.fixture
def test_shop(client, test_user):
    """Create a test shop"""
    shop = Shop(
        name='Test Shop',
        description='Test shop description',
        address='123 Test St',
        phone='1234567890',
        owner_id=test_user.id,
        is_approved=True
    )
    db.session.add(shop)
    db.session.commit()
    return shop


@pytest.fixture
def test_category(client):
    """Create a test category"""
    category = Category(name='Test Category', description='Test category')
    db.session.add(category)
    db.session.commit()
    return category


@pytest.fixture
def test_product(client, test_shop, test_category):
    """Create a test product"""
    product = Product(
        name='Test Product',
        description='Test product description',
        price=Decimal('100.00'),
        stock_quantity=100,
        shop_id=test_shop.id,
        category_id=test_category.id if test_category else None
    )
    db.session.add(product)
    db.session.commit()
    return product


@pytest.fixture
def test_order(client, test_user, test_shop, test_product):
    """Create a test order"""
    order = Order(
        order_number='ORD001',
        customer_id=test_user.id,
        shop_id=test_shop.id,
        total_amount=Decimal('200.00'),
        subtotal_amount=Decimal('200.00'),
        delivery_address='123 Test St',
        payment_status='paid',
        payment_method='mobile_money',
        status='delivered'
    )
    db.session.add(order)
    
    order_item = OrderItem(
        order_id=order.id,
        product_id=test_product.id,
        quantity=2,
        unit_price=Decimal('100.00'),
        total_price=Decimal('200.00')
    )
    db.session.add(order_item)
    db.session.commit()
    return order


class TestAnalyticsService:
    """Tests for analytics service"""
    
    def test_get_sales_overview(self, client, test_order):
        """Test getting sales overview"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        overview = AnalyticsService.get_sales_overview(start_date, end_date)
        
        assert overview is not None
        assert 'total_sales' in overview
        assert 'total_orders' in overview
        assert 'completed_orders' in overview
        assert 'avg_order_value' in overview
        assert overview['total_sales'] >= 0
        assert overview['total_orders'] >= 0
    
    def test_get_sales_trends(self, client, test_order):
        """Test getting sales trends"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        trends = AnalyticsService.get_sales_trends(start_date, end_date, 'day')
        
        assert trends is not None
        assert isinstance(trends, list)
        if trends:
            assert 'period' in trends[0]
            assert 'sales' in trends[0]
            assert 'orders' in trends[0]
    
    def test_get_top_products(self, client, test_order, test_product):
        """Test getting top products"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        products = AnalyticsService.get_top_products(limit=10, start_date=start_date, end_date=end_date)
        
        assert products is not None
        assert isinstance(products, list)
        if products:
            assert 'product_id' in products[0]
            assert 'product_name' in products[0]
            assert 'total_quantity' in products[0]
            assert 'total_revenue' in products[0]
    
    def test_get_top_shops(self, client, test_order, test_shop):
        """Test getting top shops"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        shops = AnalyticsService.get_top_shops(limit=10, start_date=start_date, end_date=end_date)
        
        assert shops is not None
        assert isinstance(shops, list)
        if shops:
            assert 'shop_id' in shops[0]
            assert 'shop_name' in shops[0]
            assert 'total_revenue' in shops[0]
            assert 'total_orders' in shops[0]
    
    def test_get_category_performance(self, client, test_order, test_category):
        """Test getting category performance"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        categories = AnalyticsService.get_category_performance(start_date, end_date)
        
        assert categories is not None
        assert isinstance(categories, list)
        if categories:
            assert 'category_id' in categories[0]
            assert 'category_name' in categories[0]
            assert 'total_revenue' in categories[0]
    
    def test_get_user_analytics(self, client, test_user):
        """Test getting user analytics"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        analytics = AnalyticsService.get_user_analytics(start_date, end_date)
        
        assert analytics is not None
        assert 'total_users' in analytics
        assert 'new_users' in analytics
        assert 'active_users' in analytics
        assert 'users_by_type' in analytics
    
    def test_get_shop_analytics(self, client, test_shop, test_order):
        """Test getting shop analytics"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        analytics = AnalyticsService.get_shop_analytics(test_shop.id, start_date, end_date)
        
        assert analytics is not None
        assert 'shop_id' in analytics
        assert 'total_orders' in analytics
        assert 'total_revenue' in analytics
        assert 'avg_order_value' in analytics
        assert 'top_products' in analytics
        assert 'sales_trends' in analytics
    
    def test_store_metric(self, client, test_shop, test_category, test_user):
        """Test storing a metric"""
        metric_date = date.today()
        metric = AnalyticsService.store_metric(
            metric_type='sales',
            metric_name='daily_sales',
            metric_value=Decimal('1000.00'),
            metric_date=metric_date,
            shop_id=test_shop.id,
            category_id=test_category.id,
            user_id=test_user.id
        )
        
        assert metric is not None
        assert metric.metric_type == 'sales'
        assert metric.metric_name == 'daily_sales'
        assert metric.metric_value == Decimal('1000.00')
        assert metric.shop_id == test_shop.id


class TestReportService:
    """Tests for report generation"""
    
    def test_generate_sales_report_pdf(self, client, test_order):
        """Test generating PDF sales report"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        buffer = ReportService.generate_sales_report(start_date, end_date, None, 'pdf')
        
        assert buffer is not None
        assert buffer.getvalue() is not None
        assert len(buffer.getvalue()) > 0
        
        # Check PDF header
        pdf_content = buffer.getvalue()
        assert b'%PDF' in pdf_content
    
    def test_generate_sales_report_excel(self, client, test_order):
        """Test generating Excel sales report"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        buffer = ReportService.generate_sales_report(start_date, end_date, None, 'excel')
        
        assert buffer is not None
        assert buffer.getvalue() is not None
        assert len(buffer.getvalue()) > 0
        
        # Check Excel header (ZIP file format)
        excel_content = buffer.getvalue()
        assert excel_content.startswith(b'PK')  # ZIP file header
    
    def test_generate_shop_report_pdf(self, client, test_shop, test_order):
        """Test generating PDF shop report"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        buffer = ReportService.generate_shop_report(test_shop.id, start_date, end_date, 'pdf')
        
        assert buffer is not None
        assert buffer.getvalue() is not None
        assert len(buffer.getvalue()) > 0
        
        # Check PDF header
        pdf_content = buffer.getvalue()
        assert b'%PDF' in pdf_content
    
    def test_generate_shop_report_excel(self, client, test_shop, test_order):
        """Test generating Excel shop report"""
        start_date = date.today() - timedelta(days=30)
        end_date = date.today()
        
        buffer = ReportService.generate_shop_report(test_shop.id, start_date, end_date, 'excel')
        
        assert buffer is not None
        assert buffer.getvalue() is not None
        assert len(buffer.getvalue()) > 0
        
        # Check Excel header (ZIP file format)
        excel_content = buffer.getvalue()
        assert excel_content.startswith(b'PK')  # ZIP file header


class TestAnalyticsModels:
    """Tests for analytics models"""
    
    def test_analytics_metric_model(self, client, test_shop, test_category, test_user):
        """Test AnalyticsMetric model"""
        metric = AnalyticsMetric(
            metric_type='sales',
            metric_name='daily_sales',
            metric_value=Decimal('1000.00'),
            metric_date=date.today(),
            shop_id=test_shop.id,
            category_id=test_category.id,
            user_id=test_user.id
        )
        db.session.add(metric)
        db.session.commit()
        
        assert metric.id is not None
        assert metric.metric_type == 'sales'
        assert metric.metric_name == 'daily_sales'
        assert metric.metric_value == Decimal('1000.00')
        
        # Test to_dict
        metric_dict = metric.to_dict()
        assert 'id' in metric_dict
        assert 'metric_type' in metric_dict
        assert 'metric_value' in metric_dict
    
    def test_report_schedule_model(self, client, test_user, test_shop):
        """Test ReportSchedule model"""
        from datetime import time
        
        schedule = ReportSchedule(
            name='Monthly Sales Report',
            report_type='sales',
            schedule_type='monthly',
            schedule_day=1,
            schedule_time=time(9, 0),
            shop_id=test_shop.id,
            date_range_days=30,
            recipient_emails='admin@example.com',
            format='pdf',
            is_active=True,
            created_by=test_user.id
        )
        db.session.add(schedule)
        db.session.commit()
        
        assert schedule.id is not None
        assert schedule.name == 'Monthly Sales Report'
        assert schedule.report_type == 'sales'
        assert schedule.schedule_type == 'monthly'
        assert schedule.is_active is True
        
        # Test to_dict
        schedule_dict = schedule.to_dict()
        assert 'id' in schedule_dict
        assert 'name' in schedule_dict
        assert 'report_type' in schedule_dict


class TestAnalyticsAPI:
    """Tests for analytics API endpoints"""
    
    def test_get_analytics_overview(self, client, auth_client, test_order):
        """Test getting analytics overview via API"""
        client, test_user = auth_client
        
        # Make user admin
        test_user.user_type = 'admin'
        db.session.commit()
        
        response = client.get('/api/analytics/overview')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'total_sales' in data['data']
    
    def test_get_top_products(self, client, auth_client, test_order):
        """Test getting top products via API"""
        client, test_user = auth_client
        
        # Make user admin
        test_user.user_type = 'admin'
        db.session.commit()
        
        response = client.get('/api/analytics/top-products?limit=5')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert isinstance(data['data'], list)
    
    def test_get_shop_analytics(self, client, auth_client, test_shop, test_order):
        """Test getting shop analytics via API"""
        client, test_user = auth_client
        
        # Make user shop owner
        test_user.user_type = 'shop_owner'
        test_shop.owner_id = test_user.id
        db.session.commit()
        
        response = client.get(f'/api/analytics/shops/{test_shop.id}')
        
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert 'data' in data
        assert 'total_orders' in data['data']
    
    def test_generate_sales_report_api(self, client, auth_client, test_order):
        """Test generating sales report via API"""
        client, test_user = auth_client
        
        # Make user admin
        test_user.user_type = 'admin'
        db.session.commit()
        
        response = client.get('/api/reports/sales?format=pdf')
        
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert 'attachment' in response.headers.get('Content-Disposition', '')
    
    def test_generate_shop_report_api(self, client, auth_client, test_shop, test_order):
        """Test generating shop report via API"""
        client, test_user = auth_client
        
        # Make user shop owner
        test_user.user_type = 'shop_owner'
        test_shop.owner_id = test_user.id
        db.session.commit()
        
        response = client.get(f'/api/reports/shops/{test_shop.id}?format=pdf')
        
        assert response.status_code == 200
        assert response.content_type == 'application/pdf'
        assert 'attachment' in response.headers.get('Content-Disposition', '')

