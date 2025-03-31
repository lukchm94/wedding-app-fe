from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

from src.shared.database.models.base import BaseModel
from src.shared.database.models.user import User

__all__ = ["Base", "BaseModel", "User"]
