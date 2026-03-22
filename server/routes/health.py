# Health check route for the Tailspin Toys API.
# Provides a simple liveness endpoint used by OpenTelemetry collectors
# and other infrastructure tooling to verify the service is running.

from flask import jsonify, Response, Blueprint

# Create a Blueprint for health routes
health_bp = Blueprint('health', __name__)


@health_bp.route('/health', methods=['GET'])
def get_health() -> tuple[Response, int]:
    """Return the liveness status of the service.

    Returns:
        A JSON response with status 'ok' and HTTP 200.
    """
    return jsonify({"status": "ok"}), 200
