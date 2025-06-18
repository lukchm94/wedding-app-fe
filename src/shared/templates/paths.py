from pydantic import BaseModel, Field


class Admin(BaseModel):
    HOME: str = Field(default="admin/dashboard.html")
    SCHEDULE: str = Field(default="admin/set-schedule.html")
    OK: str = Field(default="admin/save-itinerary-ok.html")


class HtmlPaths(BaseModel):
    ADMIN: Admin = Admin()
