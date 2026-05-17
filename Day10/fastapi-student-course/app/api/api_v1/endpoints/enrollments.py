# app/api/api_v1/endpoints/enrollments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.enrollment import EnrollmentCreate, EnrollmentOut
from app.crud import enrollment_crud
from app.api.deps import get_db, get_current_active_user

router = APIRouter()


@router.get("/", response_model=list[EnrollmentOut])
async def list_enrollments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await enrollment_crud.get_all(db, skip, limit)


@router.post("/", response_model=EnrollmentOut)
async def create_enrollment(
    enroll_in: EnrollmentCreate,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    return await enrollment_crud.create(db, enroll_in)


@router.get("/{enroll_id}", response_model=EnrollmentOut)
async def get_enrollment(
    enroll_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user)
):
    obj = await enrollment_crud.get_by_id(db, enroll_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return obj


@router.delete("/{enroll_id}", response_model=EnrollmentOut)
async def delete_enrollment(
    enroll_id: int,
    db: AsyncSession = Depends(get_db),
    _: dict = Depends(get_current_active_user),
):
    obj = await enrollment_crud.delete(db, enroll_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return obj
