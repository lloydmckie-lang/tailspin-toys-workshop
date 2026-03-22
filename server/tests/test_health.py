# Unit tests for the health check endpoint.
# Verifies that GET /health returns the expected liveness response
# following the same patterns as other test files in this project.

import unittest
import json
from typing import Any
from flask import Flask, Response
from models import db
from routes.health import health_bp


class TestHealthRoutes(unittest.TestCase):
    """Tests for the /health liveness endpoint."""

    # API paths
    HEALTH_API_PATH: str = '/health'

    def setUp(self) -> None:
        """Set up test client and in-memory database."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        # Register the health blueprint
        self.app.register_blueprint(health_bp)

        # Initialize test client and database
        self.client = self.app.test_client()
        db.init_app(self.app)

        with self.app.app_context():
            db.create_all()

    def tearDown(self) -> None:
        """Clean up test database and ensure proper connection closure."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _get_response_data(self, response: Response) -> Any:
        """Parse JSON from a response object."""
        return json.loads(response.data)

    def test_health_returns_200(self) -> None:
        """Test that the health endpoint returns HTTP 200."""
        response = self.client.get(self.HEALTH_API_PATH)

        self.assertEqual(response.status_code, 200)

    def test_health_returns_ok_status(self) -> None:
        """Test that the health response body contains status ok."""
        response = self.client.get(self.HEALTH_API_PATH)
        data = self._get_response_data(response)

        self.assertIn('status', data)
        self.assertEqual(data['status'], 'ok')

    def test_health_response_is_json(self) -> None:
        """Test that the health endpoint returns a JSON content type."""
        response = self.client.get(self.HEALTH_API_PATH)

        self.assertIn('application/json', response.content_type)


if __name__ == '__main__':
    unittest.main()
