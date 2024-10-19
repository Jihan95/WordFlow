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
from api.v1 import bcrypt, jwt, login_manager  # type: ignore
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """
     Authenticates a user and returns a JWT token.
    
    Request Body (JSON):
        email (str): The user's email.
        password (str): The user's password.
    
    Returns:
        JSON: A JWT token if authentication is successful.
    """
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, {'error': 'Not a JSON'})
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"msg": "Missing email or password"}), 400
    user = storage.get_user_by_email(User, email)
    if user and bcrypt.check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=user.id)
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad email or password"}), 401

@app_views.route('/signup', methods=['POST'], strict_slashes=False)
def createUser():
    """
    Creates a new user with the data provided in the request body.
    
    Request Body (JSON):
        email (str): The user's email (required).
        password (str): The user's password (required).
        user_name (str): The user's name (required).
    
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
    if 'username' not in data:
        abort(400, 'Missing username')
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        email=data['email'],
        username=data['username'],
        password_hash=hashed_password
    )
    storage.new(new_user)
    new_user.save()
    return jsonify(new_user.to_dict()), 201


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def getUsers():
    """
    Retrieves all users from the storage.
    
    Returns:
        JSON: A list of dictionaries, where each dictionary represents a user's data.
    """
    users = [user.to_dict() for user in storage.all(User).values()]
    return jsonify(users), 200


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
@jwt_required()
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
    current_user_id = get_jwt_identity() 
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if str(current_user_id) != str(user_id):
        return jsonify({"msg": "You are not authorized to update this user"}), 403
    storage.delete(user)
    storage.save()
    return jsonify({}), 200

@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def updateUser(user_id):
    current_user_id = get_jwt_identity()

    user = storage.get(User, user_id)
    if not user:
        abort(404)
    
    if str(current_user_id) != str(user_id):
        return jsonify({"msg": "You are not authorized to update this user"}), 403

    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(user, key, value)
    
    storage.save()
    return jsonify(user.to_dict()), 200
