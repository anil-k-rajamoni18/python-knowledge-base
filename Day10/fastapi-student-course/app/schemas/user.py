# app/schemas/user.py
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    username: str
    email: EmailStr

    model_config = {"from_attributes": True}


class UserCreate(UserBase):
    password: str


class UserUpdate(BaseModel):
    username: str | None = None
    email: EmailStr | None = None
    password: str | None = None


class UserOut(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
