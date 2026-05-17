# app/api/api_v1/endpoints/students.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.student import StudentCreate, StudentUpdate, StudentOut
from app.crud import student_crud
from app.api.deps import get_db, get_current_active_user

router = APIRouter()


@router.get("/", response_model=list[StudentOut])
async def list_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await student_crud.get_all(db, skip, limit)


@router.post("/", response_model=StudentOut)
async def create_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await student_crud.create(db, student_in)


@router.get("/{student_id}", response_model=StudentOut)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    obj = await student_crud.get_by_id(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@router.put("/{student_id}", response_model=StudentOut)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    obj = await student_crud.get_by_id(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return await student_crud.update(db, obj, student_in)
