# app/api/api_v1/endpoints/users.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.user import UserCreate, UserUpdate, UserOut
from app.crud import user_crud
from app.api.deps import get_db, get_current_active_user

router = APIRouter()


@router.post("/", response_model=UserOut)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    existing = await user_crud.get_by_username(db, user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    return await user_crud.create(db, user_in)


@router.get("/{user_id}", response_model=UserOut)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    user = await user_crud.get_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}", response_model=UserOut)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    db_obj = await user_crud.get_by_id(db, user_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="User not found")

    return await user_crud.update(db, db_obj, user_in)
