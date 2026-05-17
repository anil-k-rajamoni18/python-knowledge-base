# app/schemas/enrollment.py
from pydantic import BaseModel


class EnrollmentBase(BaseModel):
    student_id: int
    course_id: int

    model_config = {"from_attributes": True}


class EnrollmentCreate(EnrollmentBase):
    pass


class EnrollmentOut(EnrollmentBase):
    id: int
