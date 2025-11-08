"""
Wallet API routes for wallet and transaction management.
"""
from flask import jsonify, request, current_app
from flask_login import login_required, current_user
from decimal import Decimal
from app.models import Wallet, Transaction
from app.services.wallet_service import WalletService
from app.extensions import db
from app.blueprints.api import api_bp


@api_bp.route('/wallet/balance', methods=['GET'])
@login_required
def get_wallet_balance():
    """
    Get wallet balance for current user.
    
    GET /api/wallet/balance
    """
    try:
        balance = WalletService.get_wallet_balance(current_user.id)
        
        wallet = WalletService.get_or_create_wallet(current_user.id)
        
        return jsonify({
            'balance': float(balance),
            'currency': wallet.currency,
            'wallet_id': wallet.id
        })
    except Exception as e:
        current_app.logger.error(f'Error getting wallet balance: {str(e)}')
        return jsonify({'error': 'Failed to get wallet balance'}), 500


@api_bp.route('/wallet/summary', methods=['GET'])
@login_required
def get_wallet_summary():
    """
    Get wallet summary for current user.
    
    GET /api/wallet/summary
    """
    try:
        summary = WalletService.get_wallet_summary(current_user.id)
        
        return jsonify(summary)
    except Exception as e:
        current_app.logger.error(f'Error getting wallet summary: {str(e)}')
        return jsonify({'error': 'Failed to get wallet summary'}), 500


@api_bp.route('/wallet/transactions', methods=['GET'])
@login_required
def get_transactions():
    """
    Get transactions for current user.
    
    GET /api/wallet/transactions?type=credit&page=1&limit=20
    """
    transaction_type = request.args.get('type')
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int, default=20)
    
    try:
        if page:
            pagination = WalletService.get_transactions(
                current_user.id,
                transaction_type=transaction_type,
                page=page,
                limit=limit
            )
            
            return jsonify({
                'transactions': [{
                    'id': t.id,
                    'type': t.transaction_type,
                    'amount': float(t.amount),
                    'description': t.description,
                    'reference': t.reference,
                    'status': t.status,
                    'related_type': t.related_type,
                    'related_id': t.related_id,
                    'created_at': t.created_at.isoformat()
                } for t in pagination.items],
                'page': pagination.page,
                'pages': pagination.pages,
                'per_page': pagination.per_page,
                'total': pagination.total
            })
        else:
            transactions = WalletService.get_transactions(
                current_user.id,
                transaction_type=transaction_type,
                limit=limit
            )
            
            return jsonify({
                'transactions': [{
                    'id': t.id,
                    'type': t.transaction_type,
                    'amount': float(t.amount),
                    'description': t.description,
                    'reference': t.reference,
                    'status': t.status,
                    'related_type': t.related_type,
                    'related_id': t.related_id,
                    'created_at': t.created_at.isoformat()
                } for t in transactions]
            })
    except Exception as e:
        current_app.logger.error(f'Error getting transactions: {str(e)}')
        return jsonify({'error': 'Failed to get transactions'}), 500


@api_bp.route('/wallet/credit', methods=['POST'])
@login_required
def credit_wallet():
    """
    Credit wallet with amount.
    
    POST /api/wallet/credit
    Body: { "amount": 1000, "description": "Top-up", ... }
    """
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description')
    related_type = data.get('related_type')
    related_id = data.get('related_id')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Valid amount is required'}), 400
    
    try:
        transaction = WalletService.credit_wallet(
            current_user.id,
            Decimal(str(amount)),
            description=description,
            related_type=related_type,
            related_id=related_id
        )
        
        return jsonify({
            'message': 'Wallet credited successfully',
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': float(transaction.amount),
                'reference': transaction.reference,
                'status': transaction.status,
                'created_at': transaction.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error crediting wallet: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to credit wallet'}), 500


@api_bp.route('/wallet/debit', methods=['POST'])
@login_required
def debit_wallet():
    """
    Debit wallet with amount.
    
    POST /api/wallet/debit
    Body: { "amount": 500, "description": "Payment", ... }
    """
    data = request.get_json()
    amount = data.get('amount')
    description = data.get('description')
    related_type = data.get('related_type')
    related_id = data.get('related_id')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Valid amount is required'}), 400
    
    try:
        transaction = WalletService.debit_wallet(
            current_user.id,
            Decimal(str(amount)),
            description=description,
            related_type=related_type,
            related_id=related_id
        )
        
        if not transaction:
            return jsonify({'error': 'Insufficient balance'}), 400
        
        return jsonify({
            'message': 'Wallet debited successfully',
            'transaction': {
                'id': transaction.id,
                'type': transaction.transaction_type,
                'amount': float(transaction.amount),
                'reference': transaction.reference,
                'status': transaction.status,
                'created_at': transaction.created_at.isoformat()
            }
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error debiting wallet: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to debit wallet'}), 500


@api_bp.route('/wallet/transfer', methods=['POST'])
@login_required
def transfer_between_wallets():
    """
    Transfer funds between wallets.
    
    POST /api/wallet/transfer
    Body: { "to_user_id": 2, "amount": 500, "description": "Payment" }
    """
    data = request.get_json()
    to_user_id = data.get('to_user_id')
    amount = data.get('amount')
    description = data.get('description')
    
    if not to_user_id or not amount or amount <= 0:
        return jsonify({'error': 'Valid recipient user ID and amount are required'}), 400
    
    if to_user_id == current_user.id:
        return jsonify({'error': 'Cannot transfer to yourself'}), 400
    
    try:
        success, error_msg, transactions = WalletService.transfer_between_wallets(
            current_user.id,
            to_user_id,
            Decimal(str(amount)),
            description=description
        )
        
        if not success:
            return jsonify({'error': error_msg}), 400
        
        return jsonify({
            'message': 'Transfer completed successfully',
            'transactions': [{
                'id': t.id,
                'type': t.transaction_type,
                'amount': float(t.amount),
                'reference': t.reference,
                'status': t.status,
                'created_at': t.created_at.isoformat()
            } for t in transactions]
        }), 201
    except Exception as e:
        current_app.logger.error(f'Error transferring funds: {str(e)}')
        db.session.rollback()
        return jsonify({'error': 'Failed to transfer funds'}), 500

