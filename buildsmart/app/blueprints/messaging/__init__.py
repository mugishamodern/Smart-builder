from flask import Blueprint

messaging_bp = Blueprint('messaging', __name__)

from app.blueprints.messaging import routes
