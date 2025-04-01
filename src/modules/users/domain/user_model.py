from pydantic import BaseModel, EmailStr, Field

from .....src.shared.__app_configs import TokenTypes
from .....src.shared.utils.__validations import UserRoles


class UserModel(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    role: UserRoles = Field(default=UserRoles.GUEST)
    hashed_password: str = Field(..., min_length=8, max_length=255)

    class Config:
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True


class UserWithToken(BaseModel):
    access_token: str
    token_type: TokenTypes
    user: UserModel

    class Config:
        orm_mode = True
        use_enum_values = True
        arbitrary_types_allowed = True
