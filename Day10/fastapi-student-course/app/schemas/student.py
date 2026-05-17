# app/schemas/student.py
from pydantic import BaseModel, EmailStr


class StudentBase(BaseModel):
    full_name: str
    email: EmailStr
    age: int

    model_config = {"from_attributes": True}


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    full_name: str | None = None
    email: EmailStr | None = None
    age: int | None = None


class StudentOut(StudentBase):
    id: int
