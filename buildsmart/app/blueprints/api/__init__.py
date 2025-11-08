from flask import Blueprint

api_bp = Blueprint('api', __name__)

from app.blueprints.api import (
    routes, search_routes, order_tracking, stock_notification_routes,
    image_routes, inventory_routes, notification_routes, attachment_routes,
    invoice_routes, coupon_routes, tax_routes, wallet_routes, analytics_routes
)