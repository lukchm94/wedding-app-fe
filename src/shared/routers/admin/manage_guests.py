from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session

from ...auth.email_authentication import authenticate_admin
from ...database.config import get_db
from ...database.models.user import User
from ...server.config import templates
from ...utils.__validations import UserRoles
from ...utils.logger import logger

router = APIRouter(prefix="/manage_guests", tags=["manage_guests"])
db_session = Annotated[Session, Depends(get_db)]


@router.post("/")
async def create_guest(
    request: Request,
    db: db_session,
    email: str = "admin@example.com",  # Replace with actual email logic
):
    """
    Create a new guest.
    """
    # Authenticate the user
    authenticate_admin(email, db)

    # Placeholder for creating a guest logic
    return {"status": "success", "message": "Guest created successfully"}
    # return templates.TemplateResponse(
    #     "admin/manage_guests.html",
    #     {
    #         "request": request,
    #         "title": "Create Guest",
    #     },
    # )


@router.get("/", response_class=HTMLResponse)
async def manage_guests(
    request: Request,
    db: db_session,
    email: str = "admin@example.com",  # Replace with actual email logic
):
    """
    Manage guests page.
    """
    # Authenticate the user
    authenticate_admin(email, db)

    # Placeholder for managing guests logic
    return templates.TemplateResponse(
        "admin/manage_guests.html",
        {
            "request": request,
            "title": "Manage Guests",
        },
    )
