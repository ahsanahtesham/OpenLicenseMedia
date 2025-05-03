import pytest
from app import create_app, db
from app.models.user import User, Search

@pytest.fixture
def app():
    """Create and configure a Flask app for testing."""
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:',
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'WTF_CSRF_ENABLED': False,
    })
    
    # Create the database and tables
    with app.app_context():
        db.create_all()
        
        # Create test user
        user = User(username='testuser', email='test@example.com')
        user.set_password('password')
        db.session.add(user)
        
        # Create some test searches
        search1 = Search(query='nature', media_type='images', user_id=1)
        search2 = Search(query='music', media_type='audio', user_id=1)
        db.session.add_all([search1, search2])
        
        db.session.commit()
    
    yield app
    
    # Clean up
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

@pytest.fixture
def runner(app):
    """A test CLI runner for the app."""
    return app.test_cli_runner()

@pytest.fixture
def auth(client):
    """Authentication helper for tests."""
    class AuthActions:
        def login(self, email='test@example.com', password='password'):
            return client.post(
                '/login',
                data={'email': email, 'password': password}
            )
            
        def logout(self):
            return client.get('/logout')
    
    return AuthActions() 