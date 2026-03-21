"""
Publishers routes module.
Defines API endpoints for publisher-related operations.
"""
from flask import jsonify, Response, Blueprint
from models import Publisher
from sqlalchemy.orm import Query

# Create a Blueprint for publishers routes
publishers_bp = Blueprint('publishers', __name__)

def get_publishers_base_query() -> Query:
    """
    Create base query for publishers.
    
    Returns:
        Query: SQLAlchemy query object for publishers
    """
    return Publisher.query

@publishers_bp.route('/api/publishers', methods=['GET'])
def get_publishers() -> Response:
    """
    Get all publishers with their id and name.
    
    Returns:
        Response: JSON response containing list of publishers with id and name fields
    """
    publishers_query = get_publishers_base_query().all()
    
    # Return only id and name fields
    publishers_list = [
        {
            'id': publisher.id,
            'name': publisher.name
        }
        for publisher in publishers_query
    ]
    
    return jsonify(publishers_list)    import unittest
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