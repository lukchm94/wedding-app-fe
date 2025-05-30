from pydantic import BaseModel, Field

from src.shared.utils.__validations import UserRoles


class LoggedUser(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    role: UserRoles = Field(default=UserRoles.GUEST)
    permissions: str = Field(default="none")

    class Config:
        use_enum_values = True
        arbitrary_types_allowed = True
