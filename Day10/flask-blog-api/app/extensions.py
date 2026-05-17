# app/extensions.py
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from rq import Queue
from redis import Redis

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)
# simple RQ wrapper; instantiate Redis connection later in create_app via config
class RQWrapper:
    def __init__(self):
        self._queue = None
    def init_app(self, app):
        redis_url = app.config.get("REDIS_URL")
        redis_conn = Redis.from_url(redis_url)
        self._queue = Queue(connection=redis_conn)
    @property
    def queue(self):
        return self._queue

rq = RQWrapper()
