from enum import Enum

from sqlalchemy import VARCHAR, Column
from sqlalchemy import Enum as SQLEnum
from sqlalchemy import String
from sqlalchemy.orm import relationship

from src.shared.database.models.base import BaseModel


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class User(BaseModel):
    __tablename__ = "users"

    username = Column(VARCHAR(50), unique=True, nullable=False, index=True)
    email = Column(VARCHAR(255), unique=True, nullable=False, index=True)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.USER)
    hashed_password = Column(VARCHAR(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
