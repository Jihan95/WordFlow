import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pytest
from flask import Flask
from models import storage
from models.user import User
from api.v1 import app


@pytest.fixture(scope='module')
def test_client():
    flask_app = app
    flask_app.config['TESTING'] = True

    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            storage.reload()  # Initialize the DB storage for testing
        yield testing_client
        # Teardown - you can delete test data or reset database if necessary
        storage.close()


@pytest.fixture
def new_user():
    """
    Fixture to create a new user for testing purposes.
    """
    user = User(email="test_user@example.com", password="password123", username= "testuser")
    storage.new(user)
    storage.save()
    return user


def test_create_user(test_client):
    """
    Test for creating a new user via POST request to /users
    """
    user_data = {
        "email": "newuser@example.com",
        "password": "newpassword"
    }
    response = test_client.post('/users', json=user_data)
    assert response.status_code == 201
    data = response.get_json()
    assert data['email'] == user_data['email']
    assert 'id' in data  # Check if the ID is generated


def test_get_all_users(test_client, new_user):
    """
    Test retrieving all users via GET request to /users
    """
    response = test_client.get('/users')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert any(user['email'] == "test_user@example.com" for user in data)


def test_get_user_by_id(test_client, new_user):
    """
    Test retrieving a user by ID via GET request to /users/<user_id>
    """
    user_id = new_user.id
    response = test_client.get(f'/users/{user_id}')
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == new_user.email


def test_update_user(test_client, new_user):
    """
    Test updating an existing user via PUT request to /users/<user_id>
    """
    user_id = new_user.id
    update_data = {"email": "updated_user@example.com"}
    response = test_client.put(f'/users/{user_id}', json=update_data)
    assert response.status_code == 200
    data = response.get_json()
    assert data['email'] == update_data['email']


def test_delete_user(test_client, new_user):
    """
    Test deleting a user via DELETE request to /users/<user_id>
    """
    user_id = new_user.id
    response = test_client.delete(f'/users/{user_id}')
    assert response.status_code == 200
    response = test_client.get(f'/users/{user_id}')
    assert response.status_code == 404  # Ensure user is deleted


def test_get_user_by_email():
    """
    Test the get_user_by_email method from DBStorage
    """
    user = storage.get_user_by_email(User, "test_user@example.com")
    assert user is not None
    assert user.email == "test_user@example.com"
