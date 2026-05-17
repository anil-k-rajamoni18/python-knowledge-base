# app/main.py
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_v1.api import api_router
from app.db.session import engine as async_engine
from app.db.base import Base

logger = logging.getLogger("uvicorn.error")

app = FastAPI(
    title="Student Course Management API",
    description="API-only FastAPI project for managing students, courses and enrollments.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - keep permissive for development; lock down origins in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# include API router
app.include_router(api_router, prefix="/api/v1")


@app.on_event("startup")
async def on_startup():
    """
    Create database tables on startup. In production you should use Alembic migrations
    instead of creating tables at app startup.
    """
    try:
        logger.info("Creating database tables (if not present)...")
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables created/verified.")
    except Exception as e:
        logger.exception("Error creating database tables: %s", e)
        raise


@app.on_event("shutdown")
async def on_shutdown():
    # Place to close resources if needed
    logger.info("Shutting down application.")


@app.get("/", tags=["root"])
async def root():
    return {"message": "Student Course Management API", "version": "1.0.0"}


@app.get("/healthcheck", tags=["root"])
async def healthcheck():
    return {"status": "ok"}
