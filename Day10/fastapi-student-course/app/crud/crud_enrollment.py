# app/crud/crud_enrollment.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.enrollment import Enrollment
from app.schemas.enrollment import EnrollmentCreate


class CRUDEnrollment:
    async def get_by_id(self, db: AsyncSession, enroll_id: int):
        return await db.get(Enrollment, enroll_id)

    async def get_all(self, db: AsyncSession, skip=0, limit=100):
        result = await db.execute(select(Enrollment).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: EnrollmentCreate):
        db_obj = Enrollment(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, enroll_id: int):
        obj = await self.get_by_id(db, enroll_id)
        if not obj:
            return None

        await db.delete(obj)
        await db.commit()
        return obj


enrollment_crud = CRUDEnrollment()
