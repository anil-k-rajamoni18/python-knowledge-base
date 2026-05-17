import asyncio
import os
import tempfile
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.main import app
from app.db import base as db_base
from app.db import session as db_session_module
from app.api.deps import get_db as original_get_db

# Use a temporary sqlite file for tests (safer than in-memory with multiple connections)
TMP_DB = os.path.join(tempfile.gettempdir(), "test_app.db")
TEST_DATABASE_URL = f"sqlite+aiosqlite:///{TMP_DB}"

# Create a new async engine and session factory for tests
test_engine = create_async_engine(TEST_DATABASE_URL, future=True, echo=False)
AsyncSessionTestLocal = sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

@pytest.fixture(scope="session")
def event_loop():
    # Use a global event loop for pytest-asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    # Ensure DB file is removed, then create tables
    try:
        if os.path.exists(TMP_DB):
            os.remove(TMP_DB)
    except Exception:
        pass

    async with test_engine.begin() as conn:
        # Import models through db_base; set metadata to the test engine
        await conn.run_sync(db_base.Base.metadata.create_all)

    yield

    # Teardown: dispose engine & remove file
    await test_engine.dispose()
    try:
        if os.path.exists(TMP_DB):
            os.remove(TMP_DB)
    except Exception:
        pass

@pytest.fixture()
async def db_session():
    async with AsyncSessionTestLocal() as session:
        yield session

# Override FastAPI dependency to use test DB
async def _override_get_db():
    async with AsyncSessionTestLocal() as session:
        yield session

@pytest.fixture(autouse=True)
def override_dependency():
    # override dependency on the app for the duration of tests
    app.dependency_overrides[original_get_db] = _override_get_db
    yield
    app.dependency_overrides.pop(original_get_db, None)
