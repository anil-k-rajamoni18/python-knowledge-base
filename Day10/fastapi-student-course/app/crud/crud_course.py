# app/crud/crud_course.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.course import Course
from app.schemas.course import CourseCreate, CourseUpdate


class CRUDCourse:
    async def get_by_id(self, db: AsyncSession, course_id: int):
        return await db.get(Course, course_id)

    async def get_all(self, db: AsyncSession, skip=0, limit=100):
        result = await db.execute(select(Course).offset(skip).limit(limit))
        return result.scalars().all()

    async def create(self, db: AsyncSession, obj_in: CourseCreate):
        db_obj = Course(**obj_in.model_dump())
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(self, db: AsyncSession, db_obj: Course, obj_in: CourseUpdate):
        data = obj_in.model_dump(exclude_unset=True)

        for field, value in data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, course_id: int):
        obj = await self.get_by_id(db, course_id)
        if not obj:
            return None

        await db.delete(obj)
        await db.commit()
        return obj


course_crud = CRUDCourse()
