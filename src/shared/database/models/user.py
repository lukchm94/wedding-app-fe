from sqlalchemy import VARCHAR, Column
from sqlalchemy import Enum as SQLEnum

from ...utils.__validations import UserRoles
from .base_model import BaseModel


class User(BaseModel):
    __tablename__ = "users"

    username = Column(VARCHAR(50), unique=True, nullable=False, index=True)
    email = Column(VARCHAR(255), unique=True, nullable=False, index=True)
    role = Column(SQLEnum(UserRoles), nullable=False, default=UserRoles.GUEST)
    hashed_password = Column(VARCHAR(255), nullable=False)

    def __repr__(self):
        return f"<User {self.username}>"
