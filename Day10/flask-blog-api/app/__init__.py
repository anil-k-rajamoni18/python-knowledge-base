# app/__init__.py
from flask import Flask, jsonify
from .config import Config
from .extensions import db, migrate, jwt, cors, limiter, rq
from .auth import routes as auth_routes
from .posts import routes as post_routes
from .comments import routes as comment_routes
from .admin import routes as admin_routes
import logging
from logging.handlers import RotatingFileHandler
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # init extensions
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)
    limiter.init_app(app)
    rq.init_app(app)

    # register blueprints
    app.register_blueprint(auth_routes.bp, url_prefix="/api/auth")
    app.register_blueprint(post_routes.bp, url_prefix="/api/posts")
    app.register_blueprint(comment_routes.bp, url_prefix="/api/comments")
    app.register_blueprint(admin_routes.bp, url_prefix="/api/admin")

    # logging
    if not os.path.exists("logs"):
        os.mkdir("logs")
    file_handler = RotatingFileHandler("logs/blog_api.log", maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info("Blog API startup")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"msg":"Not Found"}), 404

    @app.errorhandler(429)
    def ratelimit_handler(e):
        return jsonify({"msg":"Rate limit exceeded", "detail": str(e)}), 429

    return app
