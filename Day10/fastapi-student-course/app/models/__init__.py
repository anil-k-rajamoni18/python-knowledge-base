from .user import User
from .student import Student
from .course import Course
from .enrollment import Enrollment

__all__ = ["User", "Student", "Course", "Enrollment"] # Means ? import * will only import these names
