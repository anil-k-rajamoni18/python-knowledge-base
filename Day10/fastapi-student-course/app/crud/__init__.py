from .crud_user import user_crud
from .crud_student import student_crud
from .crud_course import course_crud
from .crud_enrollment import enrollment_crud

__all__ = [
    "user_crud",
    "student_crud",
    "course_crud",
    "enrollment_crud",
]
