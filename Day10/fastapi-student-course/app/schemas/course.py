# app/schemas/course.py
from pydantic import BaseModel


class CourseBase(BaseModel):
    title: str
    description: str

    model_config = {"from_attributes": True}


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    title: str | None = None
    description: str | None = None


class CourseOut(CourseBase):
    id: int
