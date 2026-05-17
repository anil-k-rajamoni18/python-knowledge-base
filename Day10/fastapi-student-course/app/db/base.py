# app/db/base.py
from app.models.user import User
from app.models.student import Student
from app.models.course import Course
from app.models.enrollment import Enrollment
from sqlalchemy.orm import declarative_base

# The imports ensure SQLAlchemy registers all models.
# Alembic or initial DB creation should import this module.


Base = declarative_base()