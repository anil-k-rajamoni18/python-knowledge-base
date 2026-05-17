# app/posts/routes.py
from flask import Blueprint, request, jsonify, current_app
from ..models import Post, User
from ..extensions import db, limiter
from ..posts.schemas import PostCreateSchema, PostUpdateSchema
from marshmallow import ValidationError
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..utils import paginate_query, log_event

bp = Blueprint("posts", __name__)
create_schema = PostCreateSchema()
update_schema = PostUpdateSchema()

@bp.route("/", methods=["GET"])
def list_posts():
    page = request.args.get("page", 1)
    per_page = request.args.get("per_page", current_app.config.get("POSTS_PER_PAGE", 10))
    query = Post.query.order_by(Post.created_at.desc())
    posts = paginate_query(query, page, per_page)
    return jsonify([p.to_dict() for p in posts]), 200

@bp.route("/", methods=["POST"])
@jwt_required()
@limiter.limit("10 per minute")
def create_post():
    try:
        data = create_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not found"}), 404
    post = Post(title=data["title"], body=data["body"], author=user)
    db.session.add(post)
    db.session.commit()
    log_event(f"Post created: {post.title} by {user.username}")
    return jsonify(post.to_dict()), 201

@bp.route("/<int:post_id>", methods=["GET"])
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict(include_comments=True)), 200

@bp.route("/<int:post_id>", methods=["PUT"])
@jwt_required()
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    if post.author_id != user_id:
        return jsonify({"msg":"Permission denied"}), 403
    try:
        data = update_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    if "title" in data:
        post.title = data["title"]
    if "body" in data:
        post.body = data["body"]
    db.session.commit()
    log_event(f"Post updated: {post.title}")
    return jsonify(post.to_dict()), 200

@bp.route("/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if post.author_id != user_id and not user.is_admin:
        return jsonify({"msg":"Permission denied"}), 403
    db.session.delete(post)
    db.session.commit()
    log_event(f"Post deleted: {post.title}")
    return jsonify({"msg":"Deleted"}), 200
