from typing import Annotated, List

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.modules.guests.application.create_guest.create_guest_use_case import (
    CreateGuestUseCase,
)
from src.modules.guests.application.update_guest.update_guest_use_case import (
    UpdateGuestUseCase,
)
from src.modules.guests.domain.guest import Guest
from src.shared.auth.authenticate import admin_dependency
from src.shared.controllers.admin.add_guests import GuestController, GuestCreate
from src.shared.database.config import get_db
from src.shared.server.config import di_container, templates
from src.shared.utils.__validations import MenuChoices

router = APIRouter(prefix="/add-guests", tags=["admin"])
db_session = Annotated[Session, Depends(get_db)]
logger = di_container.get_logger()

# Store uploaded guests in memory (in a real app, you might use a database or session)
uploaded_guests = {
    "main_guests": [],
    "plus_ones": [],
    "failed_guests": [],
    "successful_guests": [],
    "error_message": "",
}


@router.post("/")
async def create_guest(
    request: Request,
    guest_data: GuestCreate,
    db: db_session,
    current_admin: admin_dependency,
) -> JSONResponse:
    """
    Create a new guest with optional plus-one.
    """
    logger.info(f"Received guest data: {guest_data.model_dump()}")

    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    try:
        create_guest: CreateGuestUseCase = di_container.build_create_guest_use_case(db)
        update_guest: UpdateGuestUseCase = di_container.build_update_guest_use_case(db)
        guest_controller: GuestController = di_container.build_guest_controller()

        # Convert the input data to match the Guest domain model
        guest: Guest = guest_controller.create_guest(guest_data)

        logger.info(f"Created Guest domain model: {guest.model_dump()}")
        # Pass the Guest object to the use case
        created_guest: Guest = create_guest.execute(guest)

        logger.info(f"\n\nCreated Guest domain model: {created_guest.model_dump()}\n\n")

        # Store the main guest in the uploaded_guests list
        uploaded_guests["main_guests"].append(
            {
                "first_name": created_guest.first_name,
                "last_name": created_guest.last_name,
                "email": created_guest.email,
                "has_guest": created_guest.has_guest,
            }
        )

        # Also store in successful guests
        uploaded_guests["successful_guests"].append(
            {
                "first_name": created_guest.first_name,
                "last_name": created_guest.last_name,
                "email": created_guest.email,
            }
        )

        # If there's plus-one data, create the plus-one guest and update the main guest
        if not guest_data.has_guest and not guest_data.plus_one_data:
            """
            If the guest is not bringing a plus-one, return the created guest
            """
            logger.debug(
                f"Guest is not bringing a plus-one. Returning created guest: {created_guest.model_dump()}"
            )
            return JSONResponse(
                content={
                    "status": "success",
                    "message": "Guest created successfully",
                    "data": created_guest.id,
                },
                status_code=201,
            )

        # Create the plus-one guest
        plus_one: Guest = guest_controller.create_plus_one(guest_data, created_guest.id)
        logger.info(f"Created Plus-One domain model: {plus_one.model_dump()}")

        # Create the plus-one guest
        created_plus_one: Guest = create_guest.execute(plus_one)

        # Store the plus-one in the uploaded_guests list
        uploaded_guests["plus_ones"].append(
            {
                "first_name": created_plus_one.first_name,
                "last_name": created_plus_one.last_name,
                "email": created_plus_one.email,
            }
        )

        # Also store in successful guests
        uploaded_guests["successful_guests"].append(
            {
                "first_name": created_plus_one.first_name,
                "last_name": created_plus_one.last_name,
                "email": created_plus_one.email,
            }
        )

        logger.info("\n\n\n\n")

        # Update the main guest with the plus-one ID
        created_guest.guest_id = created_plus_one.id
        logger.info(f"\n\nUpdated Guest domain model: {created_guest.model_dump()}\n\n")
        updated_guest: Guest = update_guest.execute(created_guest)

        logger.info("\n\n\n\n")

        return JSONResponse(
            content={
                "status": "success",
                "message": "Guest and plus-one created successfully",
                "data": {
                    "guest": updated_guest.id,
                    "plus_one": created_plus_one.id,
                },
            },
            status_code=201,
        )

    except ValueError as e:
        logger.error(f"Error creating guest: {str(e)}")
        # Store the failed guest
        uploaded_guests["failed_guests"].append(
            {
                "first_name": guest_data.guest_data.first_name,
                "last_name": guest_data.guest_data.last_name,
                "email": guest_data.guest_data.email,
            }
        )
        uploaded_guests["error_message"] = str(e)
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=400,
        )
    except Exception as e:
        logger.error(f"Unexpected error creating guest: {str(e)}")
        # Store the failed guest
        uploaded_guests["failed_guests"].append(
            {
                "first_name": guest_data.guest_data.first_name,
                "last_name": guest_data.guest_data.last_name,
                "email": guest_data.guest_data.email,
            }
        )
        uploaded_guests["error_message"] = "An unexpected error occurred"
        return JSONResponse(
            content={"status": "error", "message": "An unexpected error occurred"},
            status_code=500,
        )


@router.get("/failed", response_class=HTMLResponse)
async def guest_upload_failed(
    request: Request,
    current_admin: admin_dependency,
):
    """
    Display the failure page with the failed guests.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    # Get the uploaded guests from the session
    main_guests = uploaded_guests["main_guests"]
    plus_ones = uploaded_guests["plus_ones"]
    failed_guests = uploaded_guests["failed_guests"]
    successful_guests = uploaded_guests["successful_guests"]
    error_message = uploaded_guests["error_message"]

    # Clear the uploaded guests after displaying them
    uploaded_guests["main_guests"] = []
    uploaded_guests["plus_ones"] = []
    uploaded_guests["failed_guests"] = []
    uploaded_guests["successful_guests"] = []
    uploaded_guests["error_message"] = ""

    return templates.TemplateResponse(
        "admin/guest_upload_failed.html",
        {
            "request": request,
            "admin": current_admin,
            "main_guests": main_guests,
            "plus_ones": plus_ones,
            "failed_guests": failed_guests,
            "successful_guests": successful_guests,
            "error_message": error_message,
        },
    )


@router.get("/success", response_class=HTMLResponse)
async def guest_upload_success(
    request: Request,
    current_admin: admin_dependency,
):
    """
    Display the success page with the uploaded guests.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    # Get the uploaded guests from the session
    main_guests = uploaded_guests["main_guests"]
    plus_ones = uploaded_guests["plus_ones"]

    # Clear the uploaded guests after displaying them
    uploaded_guests["main_guests"] = []
    uploaded_guests["plus_ones"] = []
    uploaded_guests["failed_guests"] = []
    uploaded_guests["successful_guests"] = []
    uploaded_guests["error_message"] = ""

    return templates.TemplateResponse(
        "admin/guest_upload_success.html",
        {
            "request": request,
            "admin": current_admin,
            "main_guests": main_guests,
            "plus_ones": plus_ones,
        },
    )


@router.get("/", response_class=HTMLResponse)
async def add_guests(
    request: Request,
    current_admin: admin_dependency,
):
    """
    Serve the add guests page.
    Only accessible to authenticated admin users.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin
    logger.info(f"Rendering add guests page")
    # Get all menu choices from the enum
    menu_choices = [
        {"value": choice.value, "label": choice.value} for choice in MenuChoices
    ]

    logger.info(f"Menu choices: {menu_choices}")

    return templates.TemplateResponse(
        "admin/add_guests.html",
        {
            "request": request,
            "admin": current_admin,
            "menu_choices": menu_choices,
        },
    )
