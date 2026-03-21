# Routes for the categories resource, exposing available game categories.
from flask import jsonify, Response, Blueprint
from models import db, Category

# Create a Blueprint for categories routes
categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/api/categories', methods=['GET'])
def get_categories() -> Response:
    """Return all categories as a list of id/name objects."""
    categories = db.session.query(Category).order_by(Category.name).all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])
