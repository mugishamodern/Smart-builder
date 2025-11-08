"""
Pytest configuration and fixtures for BuildSmart tests.
"""
import pytest
from app import create_app
from app.extensions import db as _db
from app.models import User
from flask import Flask


@pytest.fixture(scope='session')
def app():
    """Create application for testing."""
    app = create_app('testing')
    with app.app_context():
        _db.create_all()
        yield app
        _db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Create test client."""
    return app.test_client()


@pytest.fixture(scope='function')
def db(app):
    """Create database for testing."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.session.remove()
        _db.drop_all()


@pytest.fixture
def test_user(db):
    """Create a test user."""
    from app.extensions import bcrypt
    user = User(
        username='testuser',
        email='test@example.com',
        full_name='Test User',
        user_type='customer'
    )
    user.set_password('TestPass123!')
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def db_session(db):
    """Provide database session."""
    return db.session


@pytest.fixture
def auth_client(client, db):
    """Create authenticated test client."""
    # Create a test user
    from app.extensions import bcrypt
    test_user = User(
        username='testuser',
        email='test@example.com',
        password_hash=bcrypt.generate_password_hash('testpass123').decode('utf-8'),
        full_name='Test User',
        user_type='customer'
    )
    db.session.add(test_user)
    db.session.commit()
    
    # Login
    client.post('/auth/login', data={
        'username': 'testuser',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    return client, test_user
