# Routes for the publishers resource, exposing available game publishers.
from flask import jsonify, Response, Blueprint
from models import db, Publisher

# Create a Blueprint for publishers routes
publishers_bp = Blueprint("publishers", __name__)

@publishers_bp.route("/api/publishers", methods=["GET"])
def get_publishers() -> Response:
    """Return all publishers as a list of id/name objects."""
    publishers = db.session.query(Publisher).order_by(Publisher.name).all()
    return jsonify([{"id": p.id, "name": p.name} for p in publishers])
