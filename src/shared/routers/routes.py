from pydantic import BaseModel, Field


class Admin(BaseModel):
    pass


class Routes(BaseModel):
    admin: Admin = Admin()
    home: str = Field(default="/")
