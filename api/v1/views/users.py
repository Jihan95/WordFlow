"""
API Views for User Management
This module defines various routes to manage users using
the RESTful API. It allows retrieving, creating, updating,
and deleting user data by interacting with the User model.
"""
from models.user import User  # type: ignore
from api.v1.views import app_views  # type: ignore
from models import storage  # type: ignore
from flask import jsonify, abort, request


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """
    Retrieves all users from the storage.
    
    Returns:
        JSON: A list of dictionaries, where each dictionary represents a user's data.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users)


@app_views.route('/users/<user_id>', methods=['GET'])
def getUserWithID(user_id):
    """
    Retrieves a specific user by their user_id.
    
    Args:
        user_id (str): The ID of the user to retrieve.
    
    Returns:
        JSON: A dictionary representing the user's data if the user is found.
    
    Raises:
        404: If the user with the given ID does not exist.
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def deleteUserWithID(user_id):
    """
    Deletes a specific user by their user_id.
    
    Args:
        user_id (str): The ID of the user to delete.
    
    Returns:
        JSON: An empty JSON object with status code 200 if the deletion is successful.
    
    Raises:
        404: If the user with the given ID does not exist.

    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def createUser():
    """
    Creates a new user with the data provided in the request body.
    
    Request Body (JSON):
        email (str): The user's email (required).
        password (str): The user's password (required).
    
    Returns:
        JSON: A dictionary representing the newly created user's data.
    
    Raises:
        400: If the request body is not JSON or if required fields (email, password) are missing.
    """
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, {'error': 'Not a JSON'})
    if 'email' not in data:
        abort(400, 'Missing email')
    if 'password' not in data:
        abort(400, 'Missing password')
    new_user = User(**data)
    storage.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def updateUser(user_id):
    """
    Updates an existing user's data with the values provided in the request body.
    
    Args:
        user_id (str): The ID of the user to update.
    
    Request Body (JSON):
        Any valid user attributes (e.g., email, first_name, last_name, etc.).
        Fields such as id, created_at, and updated_at cannot be updated.
    
    Returns:
        JSON: A dictionary representing the updated user's data.
    
    Raises:
        404: If the user with the given ID does not exist.
        400: If the request body is not JSON or is empty.
    """
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    storage.save()
    return jsonify(user.to_dict()), 200
