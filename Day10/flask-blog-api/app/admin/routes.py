# app/admin/routes.py
from flask import Blueprint, jsonify
from ..models import User, Post
from ..extensions import db
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("admin", __name__)

def admin_required(fn):
    from functools import wraps
    from flask import jsonify
    @wraps(fn)
    @jwt_required()
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()
        user = User.query.get(user_id)
        if not user or not user.is_admin:
            return jsonify({"msg":"Admin access required"}), 403
        return fn(*args, **kwargs)
    return wrapper

@bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

@bp.route("/promote/<int:user_id>", methods=["POST"])
@admin_required
def promote(user_id):
    u = User.query.get_or_404(user_id)
    u.is_admin = True
    db.session.commit()
    return jsonify({"msg":"Promoted"}), 200
