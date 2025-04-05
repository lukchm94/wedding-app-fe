from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
from sqlalchemy.orm import Session

from src.modules.guests.application.create_guest.create_guest_use_case import (
    CreateGuestUseCase,
)
from src.modules.guests.domain.guest import Guest
from src.shared.auth.authenticate import admin_dependency
from src.shared.database.config import get_db
from src.shared.server.config import di_container, templates
from src.shared.utils.__validations import MenuChoices

router = APIRouter(prefix="/manage-guests", tags=["admin"])
db_session = Annotated[Session, Depends(get_db)]
logger = di_container.get_logger()


class GuestCreate(BaseModel):
    first_name: str
    last_name: str
    email: str
    phone: str
    menu: str
    dietary_requirements: str | None = None
    needs_hotel: bool
    has_guest: bool


@router.post("/")
async def create_guest(
    request: Request,
    guest_data: GuestCreate,
    db: db_session,
    current_admin: admin_dependency,
) -> JSONResponse:
    """
    Create a new guest.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    try:
        create_guest_use_case: CreateGuestUseCase = (
            di_container.build_create_guest_use_case(db)
        )
        # Convert the input data to match the Guest domain model
        guest_dict = {
            "first_name": guest_data.first_name,
            "last_name": guest_data.last_name,
            "email": guest_data.email,
            "phone": guest_data.phone,
            "menu": MenuChoices(guest_data.menu),
            "dietary_requirements": guest_data.dietary_requirements,
            "needs_hotel": guest_data.needs_hotel,
            "has_guest": guest_data.has_guest,
            "guest_id": None,  # This will be updated later if needed
        }

        logger.info(f"Guest dictionary: {guest_dict}")
        # Create a Guest object from the dictionary using the static method
        guest_obj = Guest.from_dict(guest_dict)
        logger.info(f"Guest object: {guest_obj}")
        # Pass the Guest object to the use case
        guest: Guest = create_guest_use_case.execute(guest_obj)

        return JSONResponse(
            content={
                "status": "success",
                "message": "Guest created successfully",
                "data": guest.model_dump(),
            },
            status_code=201,
        )

    except ValueError as e:
        logger.error(f"Error creating guest: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=400,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating guest: {str(e)}")
        return JSONResponse(
            content={"status": "error", "message": "An unexpected error occurred"},
            status_code=500,
        )


@router.get("/", response_class=HTMLResponse)
async def manage_guests(
    request: Request,
    current_admin: admin_dependency,
):
    """
    Serve the manage guests page.
    Only accessible to authenticated admin users.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin
    logger.info(f"Rendering manage guests page")
    # Get all menu choices from the enum
    menu_choices = [
        {"value": choice.value, "label": choice.value} for choice in MenuChoices
    ]

    logger.info(f"Menu choices: {menu_choices}")

    return templates.TemplateResponse(
        "admin/manage_guests.html",
        {
            "request": request,
            "admin": current_admin,
            "menu_choices": menu_choices,
        },
    )
