import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import engine, AsyncSessionLocal
from app.db import base
from app.core.config import get_settings
from app.crud import user_crud
from app.schemas.user import UserCreate


settings = get_settings()


async def init_db():
    """Create tables and seed initial superuser."""
    # Create DB schema
    async with engine.begin() as conn:
        await conn.run_sync(base.Base.metadata.create_all)

    # Create initial superuser
    async with AsyncSessionLocal() as db:
        existing = await user_crud.get_by_username(db, settings.FIRST_SUPERUSER)
        if not existing:
            superuser = UserCreate(
                username=settings.FIRST_SUPERUSER,
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
            )
            print("Creating initial superuser...")
            await user_crud.create(db, superuser)
        else:
            print("Superuser already exists. Skipping.")


def main():
    print("Initializing database...")
    asyncio.run(init_db())
    print("Initial data created.")


if __name__ == "__main__":
    main()
