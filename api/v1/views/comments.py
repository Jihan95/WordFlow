"""
API Views for Comment Management
This module defines various routes to manage comments using
the RESTful API. It allows retrieving, creating, updating,
and deleting user comment by interacting with the Comment model.
"""
from models.user import User  # type: ignore
from models.post import Post  # type: ignore
from models.comment import Comment  # type: ignore
from api.v1.views import app_views  # type: ignore
from models import storage  # type: ignore
from flask import jsonify, abort, request
from api.v1 import bcrypt, jwt, login_manager  # type: ignore
from flask_jwt_extended import jwt_required, get_jwt_identity


@app_views.route('/posts/<post_id>/comments', methods=['POST'], strict_slashes=False)
@jwt_required()
def addComment(post_id):
    """
    Adds a new comment to the post specified by `post_id`.
    
    The comment content must be provided in the request's JSON body.
    
    Route:
    POST /posts/<post_id>/comments
    
    Request JSON format:
    {
        "content": "Your comment text here"
    }
    
    Responses:
    - 201: Comment created successfully.
    - 400: Invalid data (e.g., missing content).
    - 404: Post not found.
    - 401: User not logged in.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'msg': 'Unauthorized access'}), 401
    post = storage.get(Post, post_id)
    if not post:
        abort(404, {'error': 'Post not found'})
    data = request.get_json()
    if not data or not isinstance(data, dict):
        abort(400, {'error': 'Not a valid JSON'})
    if 'content' not in data:
        jsonify({'error': 'Missing content'}), 400
    new_comment = Comment(
        post_id=post.id,
        user_id=current_user_id,
        content=data['content']
    )
    storage.new(new_comment)
    new_comment.save()
    return jsonify(new_comment.to_dict()), 201
    

@app_views.route('/posts/<post_id>/comments', methods=['GET'], strict_slashes=False)
@jwt_required()
def getAllComments(post_id):
    """
    Retrieves all comments for a specific post by `post_id`.

    Returns:
    - 200: A list of comments in JSON format.
    - 404: Post not found.
    - 401: Unauthorized access.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'msg': 'Unauthorized access'}), 401
    post = storage.get(Post, post_id)
    if not post:
        abort(404, {'error': 'Post not found'})
    comments = [comment.to_dict() for comment in post.comments]
    return jsonify(comments), 200


@app_views.route('/posts/<post_id>/comments/<comment_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def deleteComment(post_id, comment_id):
    """
    Deletes a comment identified by `comment_id` from a post identified by `post_id`.

    The user must be either the author of the post or the author of the comment to delete it.

    Responses:
    - 200: Comment deleted successfully.
    - 404: Post or comment not found.
    - 401: Unauthorized access.
    """
    current_user_id = get_jwt_identity()
    if not current_user_id:
        return jsonify({'msg': 'Unauthorized access'}), 401
    post = storage.get(Post, post_id)
    if not post:
        abort(404, {'error': 'Post not found'})
    comment = storage.get(Comment, comment_id)
    if not comment:
        abort(404, {'error': 'Comment not found'})
    if current_user_id not in [post.user_id, comment.user_id]:
        return jsonify({'msg': 'You are not authorized to delete this comment'}), 401
    storage.delete(comment)
    storage.save()
    return jsonify({}), 200
