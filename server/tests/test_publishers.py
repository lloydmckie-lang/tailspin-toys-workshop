import unittest
from server.app import create_app, db
from server.models.publisher import Publisher


class TestPublisherRoutes(unittest.TestCase):
    """Test cases for publisher API endpoints."""
    
    TEST_DATA = [
        {'name': 'Epic Games Publishing'},
        {'name': 'Devolver Digital'},
        {'name': 'Annapurna Interactive'},
    ]

    def setUp(self) -> None:
        """Set up test client and database."""
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            self._seed_test_data()

    def tearDown(self) -> None:
        """Clean up database."""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
            db.engine.dispose()

    def _seed_test_data(self) -> None:
        """Seed the database with test publishers."""
        for data in self.TEST_DATA:
            publisher = Publisher(**data)
            db.session.add(publisher)
        db.session.commit()

    def test_get_all_publishers(self) -> None:
        """Test GET /api/publishers returns all publishers."""
        response = self.client.get('/api/publishers')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), len(self.TEST_DATA))
        
        # Verify each publisher has required fields
        for publisher in data:
            self.assertIn('id', publisher)
            self.assertIn('name', publisher)
            self.assertIsInstance(publisher['id'], int)
            self.assertIsInstance(publisher['name'], str)
        
        # Verify names match test data
        names = [p['name'] for p in data]
        expected_names = [p['name'] for p in self.TEST_DATA]
        self.assertEqual(sorted(names), sorted(expected_names))

    def test_get_publishers_empty_database(self) -> None:
        """Test GET /api/publishers returns empty list when no publishers exist."""
        # Clear the database
        with self.app.app_context():
            Publisher.query.delete()
            db.session.commit()
        
        response = self.client.get('/api/publishers')
        
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 0)


if __name__ == '__main__':
    unittest.main()