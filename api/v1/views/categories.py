"""
API Views for Category Management
This module defines various routes to manage ccategories using
the RESTful API. It allows retrieving, creating, updating,
and deleting categories by interacting with the Category model.
"""
from models.user import User  # type: ignore
from models.post import Post  # type: ignore
from models.comment import Comment  # type: ignore
from models.category import Category  # type: ignore
from api.v1.views import app_views  # type: ignore
from models import storage  # type: ignore
from flask import jsonify, abort, request
from api.v1 import bcrypt, jwt, login_manager  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route('/categories', methods=['GET'], strict_slashes=False)
@jwt_required()
def getAllCategories():
    """
    Retrieves all categories.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'msg': 'Unauthorized access'}), 401
    categories = [category.to_dict() for category in storage.all(Category).values()]
    return jsonify(categories), 200


@app_views.route('/categories/<category_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def getCategoryByID(category_id):
    """
    Retrieves a specific category by its ID.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'msg': 'Unauthorized access'}), 401
    category = storage.get(Category, category_id)
    if category is None:
        abort(404, {'error': 'Category not found'})
    return jsonify(category.to_dict())
