from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.shared.database.config import engine
from src.shared.database.models import Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    # Shutdown: Close database connection
    engine.dispose()
