# Unit tests for the /api/categories endpoint.
import json
import unittest
from typing import Any
from flask import Flask, Response
from models import db, Category
from routes.categories import categories_bp


class TestCategoriesRoutes(unittest.TestCase):
    """Tests for the GET /api/categories endpoint."""

    TEST_DATA = [
        {"name": "Strategy"},
        {"name": "Card Game"},
        {"name": "RPG"},
    ]

    CATEGORIES_API_PATH: str = '/api/categories'

    def setUp(self) -> None:
        """Set up test client and in-memory database."""
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

        self.app.register_blueprint(categories_bp)
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
        """Seed the database with test categories."""
        db.session.add_all([Category(**data) for data in self.TEST_DATA])
        db.session.commit()

    def _get_response_data(self, response: Response) -> Any:
        """Parse JSON from a response."""
        return json.loads(response.data)

    def test_get_categories_success(self) -> None:
        """Test that all categories are returned with a 200 status."""
        response = self.client.get(self.CATEGORIES_API_PATH)
        data = self._get_response_data(response)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA))

    def test_get_categories_structure(self) -> None:
        """Test that each category has id and name fields."""
        response = self.client.get(self.CATEGORIES_API_PATH)
        data = self._get_response_data(response)

        for category in data:
            self.assertIn('id', category)
            self.assertIn('name', category)
            self.assertIsInstance(category['id'], int)
            self.assertIsInstance(category['name'], str)

    def test_get_categories_names_match(self) -> None:
        """Test that returned category names match seeded data."""
        response = self.client.get(self.CATEGORIES_API_PATH)
        data = self._get_response_data(response)

        returned_names = sorted([c['name'] for c in data])
        expected_names = sorted([d['name'] for d in self.TEST_DATA])
        self.assertEqual(returned_names, expected_names)

    def test_get_categories_empty_database(self) -> None:
        """Test that an empty list is returned when no categories exist."""
        with self.app.app_context():
            db.session.query(Category).delete()
            db.session.commit()

        response = self.client.get(self.CATEGORIES_API_PATH)
        data = self._get_response_data(response)

        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()
