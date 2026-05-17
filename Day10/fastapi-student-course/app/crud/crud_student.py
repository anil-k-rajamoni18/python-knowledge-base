# app/crud/crud_student.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class CRUDStudent:
    async def get_by_id(self, db: AsyncSession, student_id: int):
        return await db.get(Student, student_id)

    async def get_all(self, db: AsyncSession, skip=0, limit=100):
        result = await db.execute(select(Student).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: StudentCreate):
        db_obj = Student(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Student, obj_in: StudentUpdate):
        data = obj_in.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, student_id: int):
        obj = await self.get_by_id(db, student_id)
        if not obj:
            return None

        await db.delete(obj)
        await db.commit()
        return obj


student_crud = CRUDStudent()
