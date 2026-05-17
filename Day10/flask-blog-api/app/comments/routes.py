# app/comments/routes.py
from flask import Blueprint, request, jsonify
from ..extensions import db, limiter
from ..models import Comment, Post, User
from ..comments.schemas import CommentCreateSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import log_event

bp = Blueprint("comments", __name__)
create_schema = CommentCreateSchema()

@bp.route("/post/<int:post_id>", methods=["POST"])
@jwt_required()
@limiter.limit("30 per hour")
def add_comment(post_id):
    try:
        data = create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    comment = Comment(body=data["body"], author=user, post=post)
    db.session.add(comment)
    db.session.commit()
    log_event(f"Comment added on post {post.id} by {user.username}")
    return jsonify(comment.to_dict()), 201

@bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if comment.author_id != user_id and not user.is_admin:
        return jsonify({"msg":"Permission denied"}), 403
    db.session.delete(comment)
    db.session.commit()
    log_event(f"Comment {comment_id} deleted")
    return jsonify({"msg":"Deleted"}), 200
