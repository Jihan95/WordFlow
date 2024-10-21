"""
API Views for Post Management
This module defines various routes to manage posts using
the RESTful API. It allows retrieving, creating, updating,
and deleting posts by interacting with the POst model.
"""
from models.user import User  # type: ignore
from models.post import Post # type: ignore
from models.category import Category  # type: ignore
from api.v1.views import app_views  # type: ignore
from models import storage  # type: ignore
from flask import jsonify, abort, request
from api.v1 import bcrypt, jwt, login_manager  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route('/posts', methods=['POST'], strict_slashes=False)
@jwt_required()
def createPost():
    """
    Creates a new post with the data provided in the request body.

    Request Body (JSON):
        title (str): The post title (required)
        content (str): the post content (required)

    Returns:
        JSON: A dictionary representing the newly created post.

    Raises:
        400: If the request body is not JSON or if required fields (title, content) are missing.
        403: If the user is not allowed to perform this action.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(403, 'User not found or not authorized to create posts')
    data = request.get_json()
    if not isinstance(data, dict):
        abort(400, {'error': 'Not a JSON'})
    if 'title' not in data:
        abort(400, 'Missing Title')
    if 'content' not in data:
        abort(400, 'Missing Content')
    new_post = Post(
        user_id = current_user_id,
        title=data['title'],
        content=data['content']
        )
    storage.new(new_post)
    new_post.save()
    return jsonify(new_post.to_dict()), 201


@app_views.route('/posts', methods=['GET'], strict_slashes=False)
@jwt_required()
def getAllPosts():
    """
    Retrieves all posts.

    This endpoint returns a list of all posts from the database. The user must be authenticated via JWT.

    Returns:
        JSON: A list of dictionaries, where each dictionary represents a post.

    Raises:
        403: If the authenticated user does not exist or is not authorized to access posts.
        200: On successful retrieval of posts.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(403, 'User not found or not authorized to see posts')
    posts = [post.to_dict() for post in storage.all(Post).values()]
    return jsonify(posts), 200


@app_views.route('/posts/<post_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def getPostById(post_id):
    """
    Retrieves a specific post by their post_id.
    
    Args:
        post_id (str): The ID of the post to retrieve.
    
    Returns:
        JSON: A dictionary representing the post's data if the post is found.
    
    Raises:
        403: If the authenticated user is not authorized to view the post.
        404: If the post with the given ID does not exist.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(403, 'User not found or not authorized to view post')
    post = Post.query.get(post_id)
    if not post:
        abort(404, 'Post not found')
    return jsonify(post.to_dict()), 200


@app_views.route('/posts/<post_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def deletePostById(post_id):
    """
    Deletes a specific post by their post_id.
    
    Args:
        post_id (str): The ID of the post to delete
    
    Returns:
        JSON: An empty JSON object with status code 200 if the deletion is successful.
    
    Raises:
        403: If the authenticated user is not authorized to delete the post.
        404: If the post with the given ID does not exist.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(403, 'User not found or not authorized to delete post')
    post = storage.get(Post, post_id)
    if not post:
        abort(404, 'Post not found')
    if post.user_id != current_user_id:
        abort(403, 'You are not authorized to delete this post')
    storage.delete(post)
    storage.save()
    return jsonify({}), 200


@app_views.route('/posts/<post_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def updatePostById(post_id):
    """
    Updates a specific post by their post_id.
    
    Args:
        post_id (str): The ID of the post to delete
    
    Returns:
        JSON: an updated post
    
    Raises:
        403: If the authenticated user is not authorized to update the post.
        404: If the post with the given ID does not exist.
    """
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)
    if not user:
        abort(403, 'User not found or not authorized to delete post')
    post = Post.query.get(post_id)
    if not post:
        abort(404, 'Post not found')
    data = request.get_json()
    if not isinstance(data, dict) or not data:
        abort(400, {'error': 'Not a JSON'})
    if post.user_id != current_user_id:
        abort(403, 'You are not authorized to update this post')
    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(post, key, value)
    storage.save()
    return jsonify(post.to_dict()), 200


@app_views.route('/posts/<post_id>/categories/<category_id>', methods=['POST'], strict_slashes=False)
@jwt_required()
def assignCategorytoPost(post_id, category_id):
    """
    Assign Category to Post
    """
    current_user_id = get_jwt_identity()
    post = storage.get(Post, post_id)
    if post is None:
        abort(404, {'error': 'Post not found'})
    category = storage.get(Category, category_id)
    if category is None:
        abort(404, {'error': 'Category not found'})
    if current_user_id != post.user_id:
        abort(403, 'You are not authorized to update this post')
    if category not in post.categories:
        post.categories.append(category)
        storage.save()
    return jsonify(post.to_dict()), 200
    

@app_views.route('/posts/<post_id>/categories/<category_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def removeCtegoryFromPost(post_id, category_id):
    """
    Remove a category from a post. Only the post author can remove categories.
    """
    current_user_id = get_jwt_identity()
    post = storage.get(Post, post_id)
    if post is None:
        abort(404, {'error': 'Post not found'})
    category = storage.get(Category, category_id)
    if category is None:
        abort(404, {'error': 'Category not found'})
    if current_user_id != post.user_id:
        abort(403, 'You are not authorized to update this post')
    if category in post.categories:
        post.categories.remove(category)
        storage.save()
        return jsonify(post.to_dict()), 200
    return jsonify({'msg': 'Category not assigned to this post'}), 400
