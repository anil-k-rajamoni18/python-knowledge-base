# app/auth/routes.py
from flask import Blueprint, request, jsonify, current_app
from ..extensions import db, jwt
from ..models import User
from ..auth.schemas import RegisterSchema, LoginSchema
from marshmallow import ValidationError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from ..utils import log_event
from ..extensions import limiter

bp = Blueprint("auth", __name__)
register_schema = RegisterSchema()
login_schema = LoginSchema()

@bp.route("/register", methods=["POST"])
@limiter.limit("5 per minute")
def register():
    try:
        data = register_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    if User.query.filter((User.username==data["username"]) | (User.email==data["email"])).first():
        return jsonify({"msg":"Username or email already exists"}), 409

    user = User(username=data["username"], email=data["email"])
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    log_event(f"User registered: {user.username}")
    return jsonify({"msg":"User registered successfully"}), 201

@bp.route("/login", methods=["POST"])
@limiter.limit("10 per minute")
def login():
    try:
        data = login_schema.load(request.get_json())
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400
    user = User.query.filter_by(username=data["username"]).first()
    if not user or not user.check_password(data["password"]):
        return jsonify({"msg":"Bad username or password"}), 401
    access_token = create_access_token(identity=user.id)
    log_event(f"User logged in: {user.username}")
    return jsonify({"access_token": access_token, "user": user.to_dict()}), 200

@bp.route("/me", methods=["GET"])
@jwt_required()
def me():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    if not user:
        return jsonify({"msg":"User not found"}), 404
    return jsonify(user.to_dict()), 200
