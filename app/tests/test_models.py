import unittest
from datetime import datetime
from app import create_app, db
from app.models.user import User, Search

class TestUserModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app({
            'TESTING': True,
            'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
        })
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def test_password_hashing(self):
        user = User(username='test_user', email='test@example.com')
        user.set_password('test_password')
        self.assertFalse(user.check_password('wrong_password'))
        self.assertTrue(user.check_password('test_password'))
    
    def test_user_creation(self):
        user = User(username='test_user', email='test@example.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
        
        # Retrieve the user from database
        retrieved_user = User.query.filter_by(username='test_user').first()
        self.assertIsNotNone(retrieved_user)
        self.assertEqual(retrieved_user.email, 'test@example.com')
    
    def test_search_relationship(self):
        # Create a user
        user = User(username='test_user', email='test@example.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
        
        # Create some searches
        search1 = Search(query='nature', media_type='images', user_id=user.id)
        search2 = Search(query='music', media_type='audio', user_id=user.id)
        db.session.add_all([search1, search2])
        db.session.commit()
        
        # Check relationship
        self.assertEqual(len(user.searches), 2)
        self.assertEqual(user.searches[0].query, 'nature')
        self.assertEqual(user.searches[1].query, 'music')
    
    def test_search_cascade_delete(self):
        # Create a user with searches
        user = User(username='test_user', email='test@example.com')
        user.set_password('test_password')
        db.session.add(user)
        db.session.commit()
        
        search = Search(query='nature', media_type='images', user_id=user.id)
        db.session.add(search)
        db.session.commit()
        
        # Verify search exists
        self.assertEqual(Search.query.count(), 1)
        
        # Delete user and verify cascade
        db.session.delete(user)
        db.session.commit()
        
        # Check that search was deleted
        self.assertEqual(Search.query.count(), 0)

if __name__ == '__main__':
    unittest.main() 