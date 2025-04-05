from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.shared.database import models
from src.shared.database.config import engine
from src.shared.database.models.base import Base
from src.shared.database.models.guest import Guest  # Import the Guest model explicitly
from src.shared.database.models.user import User  # Import the User model explicitly

print(f"Initializing database models: {Base.metadata.tables.keys()}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Create database tables
    Base.metadata.create_all(
        bind=engine
    )  # This will include all models registered with Base
    yield
    # Shutdown: Close database connection
    engine.dispose()
