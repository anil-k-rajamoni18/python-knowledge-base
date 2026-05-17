# app/api/api_v1/endpoints/courses.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.course import CourseCreate, CourseUpdate, CourseOut
from app.crud import course_crud
from app.api.deps import get_db, get_current_active_user

router = APIRouter()


@router.get("/", response_model=list[CourseOut])
async def list_courses(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await course_crud.get_all(db, skip, limit)


@router.post("/", response_model=CourseOut)
async def create_course(
    course_in: CourseCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await course_crud.create(db, course_in)


@router.get("/{course_id}", response_model=CourseOut)
async def get_course(
    course_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    obj = await course_crud.get_by_id(db, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    return obj


@router.put("/{course_id}", response_model=CourseOut)
async def update_course(
    course_id: int,
    course_in: CourseUpdate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    obj = await course_crud.get_by_id(db, course_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Course not found")
    return await course_crud.update(db, obj, course_in)
