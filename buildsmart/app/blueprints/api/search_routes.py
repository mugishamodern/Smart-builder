"""
Enhanced search routes with suggestions, history, and trending searches.

This module provides enhanced search functionality including:
- Search suggestions
- Search history
- Trending searches
"""
from flask import jsonify, request
from flask_login import login_required, current_user
from app.blueprints.api import api_bp
from app.models import SearchHistory, TrendingSearch, Product, Shop
from app.extensions import db
from app.utils.error_handlers import handle_api_error
from datetime import datetime, timedelta
from sqlalchemy import func, desc


@api_bp.route('/search/suggestions', methods=['GET'])
def get_search_suggestions():
    """
    Get search suggestions based on query.
    
    Returns:
        JSON response with search suggestions
    """
    try:
        query = request.args.get('q', '').strip()
        search_type = request.args.get('type', 'products')  # products, shops, services
        limit = request.args.get('limit', 10, type=int)
        
        if not query or len(query) < 2:
            return jsonify({
                'suggestions': [],
                'trending': []
            }), 200
        
        suggestions = []
        
        # Get suggestions from product names
        if search_type == 'products':
            products = Product.query.filter(
                Product.name.ilike(f'%{query}%')
            ).limit(limit).all()
            
            suggestions = [{
                'text': p.name,
                'type': 'product',
                'id': p.id
            } for p in products]
        
        # Get suggestions from shop names
        elif search_type == 'shops':
            shops = Shop.query.filter(
                Shop.name.ilike(f'%{query}%')
            ).limit(limit).all()
            
            suggestions = [{
                'text': s.name,
                'type': 'shop',
                'id': s.id
            } for s in shops]
        
        # Get trending searches
        trending = TrendingSearch.query.filter(
            TrendingSearch.query.ilike(f'%{query}%'),
            TrendingSearch.search_type == search_type
        ).order_by(
            desc(TrendingSearch.count),
            desc(TrendingSearch.last_searched)
        ).limit(5).all()
        
        trending_list = [{
            'text': t.query,
            'count': t.count
        } for t in trending]
        
        return jsonify({
            'suggestions': suggestions,
            'trending': trending_list
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/search/history', methods=['GET'])
@login_required
def get_search_history():
    """
    Get user's search history.
    
    Returns:
        JSON response with search history
    """
    try:
        search_type = request.args.get('type')  # Optional filter
        limit = request.args.get('limit', 20, type=int)
        
        query = SearchHistory.query.filter_by(user_id=current_user.id)
        
        if search_type:
            query = query.filter_by(search_type=search_type)
        
        history = query.order_by(
            desc(SearchHistory.created_at)
        ).limit(limit).all()
        
        history_data = [{
            'id': h.id,
            'query': h.query,
            'search_type': h.search_type,
            'results_count': h.results_count,
            'created_at': h.created_at.isoformat()
        } for h in history]
        
        return jsonify({
            'history': history_data
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/search/history/<int:history_id>', methods=['DELETE'])
@login_required
def delete_search_history(history_id):
    """
    Delete a search history entry.
    
    Args:
        history_id: Search history ID
        
    Returns:
        JSON response
    """
    try:
        history = SearchHistory.query.filter_by(
            id=history_id,
            user_id=current_user.id
        ).first()
        
        if not history:
            return jsonify({
                'error': 'Search history not found'
            }), 404
        
        db.session.delete(history)
        db.session.commit()
        
        return jsonify({
            'message': 'Search history deleted'
        }), 200
        
    except Exception as e:
        return handle_api_error(e)


@api_bp.route('/search/trending', methods=['GET'])
def get_trending_searches():
    """
    Get trending searches.
    
    Returns:
        JSON response with trending searches
    """
    try:
        search_type = request.args.get('type', 'products')
        limit = request.args.get('limit', 10, type=int)
        days = request.args.get('days', 7, type=int)  # Last N days
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        trending = TrendingSearch.query.filter(
            TrendingSearch.search_type == search_type,
            TrendingSearch.last_searched >= cutoff_date
        ).order_by(
            desc(TrendingSearch.count),
            desc(TrendingSearch.last_searched)
        ).limit(limit).all()
        
        trending_data = [{
            'query': t.query,
            'count': t.count,
            'last_searched': t.last_searched.isoformat()
        } for t in trending]
        
        return jsonify({
            'trending': trending_data
        }), 200
        
    except Exception as e:
        return handle_api_error(e)

