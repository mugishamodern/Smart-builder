"""
API routes for analytics and reporting.

This module provides API endpoints for accessing analytics data
and generating reports.
"""
from flask import Blueprint, request, jsonify, send_file
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from io import BytesIO
from app.services.analytics_service import AnalyticsService
from app.services.report_service import ReportService
from app.utils.decorators import admin_required
from app.models import Shop
from app.extensions import db

# Import api_bp from __init__.py
from . import api_bp


@api_bp.route('/analytics/overview', methods=['GET'])
@login_required
@admin_required
def get_analytics_overview():
    """
    Get analytics overview.
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with analytics overview
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        overview = AnalyticsService.get_sales_overview(start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': overview
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/sales-trends', methods=['GET'])
@login_required
@admin_required
def get_sales_trends():
    """
    Get sales trends.
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        group_by: Grouping period ('day', 'week', 'month')
    
    Returns:
        JSON with sales trends data
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        group_by = request.args.get('group_by', 'day')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        trends = AnalyticsService.get_sales_trends(start_date, end_date, group_by)
        
        return jsonify({
            'success': True,
            'data': trends
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/top-products', methods=['GET'])
@login_required
@admin_required
def get_top_products():
    """
    Get top products.
    
    Query Parameters:
        limit: Number of products to return (default: 10)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with top products data
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        products = AnalyticsService.get_top_products(limit, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': products
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/top-shops', methods=['GET'])
@login_required
@admin_required
def get_top_shops():
    """
    Get top shops.
    
    Query Parameters:
        limit: Number of shops to return (default: 10)
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with top shops data
    """
    try:
        limit = request.args.get('limit', 10, type=int)
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        shops = AnalyticsService.get_top_shops(limit, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': shops
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/category-performance', methods=['GET'])
@login_required
@admin_required
def get_category_performance():
    """
    Get category performance.
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with category performance data
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        categories = AnalyticsService.get_category_performance(start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': categories
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/users', methods=['GET'])
@login_required
@admin_required
def get_user_analytics():
    """
    Get user analytics.
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with user analytics data
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        analytics = AnalyticsService.get_user_analytics(start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': analytics
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/analytics/shops/<int:shop_id>', methods=['GET'])
@login_required
def get_shop_analytics(shop_id):
    """
    Get analytics for a specific shop.
    
    Args:
        shop_id: Shop ID
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
    
    Returns:
        JSON with shop analytics data
    """
    try:
        # Check if user owns the shop or is admin
        shop = Shop.query.get_or_404(shop_id)
        if shop.owner_id != current_user.id and current_user.user_type != 'admin':
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        analytics = AnalyticsService.get_shop_analytics(shop_id, start_date, end_date)
        
        return jsonify({
            'success': True,
            'data': analytics
        }), 200
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/reports/sales', methods=['GET'])
@login_required
@admin_required
def generate_sales_report():
    """
    Generate sales report.
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        shop_id: Optional shop ID filter
        format: Report format ('pdf' or 'excel', default: 'pdf')
    
    Returns:
        Report file (PDF or Excel)
    """
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        shop_id = request.args.get('shop_id', type=int)
        format = request.args.get('format', 'pdf')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        if shop_id:
            buffer = ReportService.generate_shop_report(shop_id, start_date, end_date, format)
            filename = f'shop_report_{shop_id}_{datetime.now().strftime("%Y%m%d")}.{format}'
        else:
            buffer = ReportService.generate_sales_report(start_date, end_date, shop_id, format)
            filename = f'sales_report_{datetime.now().strftime("%Y%m%d")}.{format}'
        
        mimetype = 'application/pdf' if format == 'pdf' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        return send_file(
            buffer,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@api_bp.route('/reports/shops/<int:shop_id>', methods=['GET'])
@login_required
def generate_shop_report(shop_id):
    """
    Generate shop-specific report.
    
    Args:
        shop_id: Shop ID
    
    Query Parameters:
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        format: Report format ('pdf' or 'excel', default: 'pdf')
    
    Returns:
        Report file (PDF or Excel)
    """
    try:
        # Check if user owns the shop or is admin
        shop = Shop.query.get_or_404(shop_id)
        if shop.owner_id != current_user.id and current_user.user_type != 'admin':
            return jsonify({
                'success': False,
                'error': 'Unauthorized'
            }), 403
        
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')
        format = request.args.get('format', 'pdf')
        
        start_date = None
        end_date = None
        
        if start_date_str:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        
        buffer = ReportService.generate_shop_report(shop_id, start_date, end_date, format)
        filename = f'shop_report_{shop_id}_{datetime.now().strftime("%Y%m%d")}.{format}'
        
        mimetype = 'application/pdf' if format == 'pdf' else 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        
        return send_file(
            buffer,
            mimetype=mimetype,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

