from sqlalchemy import VARCHAR
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from ...utils.__validations import UserRoles
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        VARCHAR(50), unique=True, nullable=False, index=True
    )
    email: Mapped[str] = mapped_column(
        VARCHAR(255), unique=True, nullable=False, index=True
    )
    role: Mapped[UserRoles] = mapped_column(
        SQLEnum(UserRoles), nullable=False, default=UserRoles.GUEST
    )
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
