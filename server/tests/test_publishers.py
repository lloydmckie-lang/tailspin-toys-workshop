# Unit tests for the /api/publishers endpoint.
import json
import unittest
from typing import Any
from flask import Flask, Response
from models import db, Publisher
from routes.publishers import publishers_bp


class TestPublishersRoutes(unittest.TestCase):
    """Tests for the GET /api/publishers endpoint."""

    TEST_DATA = [
        {"name": "DevGames Inc"},
        {"name": "Scrum Masters"},
        {"name": "Pixel Forge"},
    ]

    PUBLISHERS_API_PATH: str = '/api/publishers'

    def setUp(self) -> None:
        """Set up test client and in-memory database."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app.register_blueprint(publishers_bp)
        self.client = self.app.test_client()

        db.init_app(self.app)
        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

    def tearDown(self) -> None:
        """Clean up database after each test."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _seed_test_data(self) -> None:
        """Seed the database with test publishers."""
        db.session.add_all([Publisher(**data) for data in self.TEST_DATA])
        db.session.commit()

    def _get_response_data(self, response: Response) -> Any:
        """Parse JSON from a response."""
        return json.loads(response.data)

    def test_get_publishers_success(self) -> None:
        """Test that all publishers are returned with a 200 status."""
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA))

    def test_get_publishers_structure(self) -> None:
        """Test that each publisher has id and name fields."""
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)

        for publisher in data:
            self.assertIn('id', publisher)
            self.assertIn('name', publisher)
            self.assertIsInstance(publisher['id'], int)
            self.assertIsInstance(publisher['name'], str)

    def test_get_publishers_names_match(self) -> None:
        """Test that returned publisher names match seeded data."""
        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)

        returned_names = sorted([p['name'] for p in data])
        expected_names = sorted([d['name'] for d in self.TEST_DATA])
        self.assertEqual(returned_names, expected_names)

    def test_get_publishers_empty_database(self) -> None:
        """Test that an empty list is returned when no publishers exist."""
        with self.app.app_context():
            db.session.query(Publisher).delete()
            db.session.commit()

        response = self.client.get(self.PUBLISHERS_API_PATH)
        data = self._get_response_data(response)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
