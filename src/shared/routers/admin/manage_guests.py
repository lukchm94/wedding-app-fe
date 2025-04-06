from typing import Annotated, List, Optional, Union

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.modules.guests.application.create_guest.create_guest_use_case import (
    CreateGuestUseCase,
)
from src.modules.guests.application.find_guest.find_guest_use_case import (
    FindGuestUseCase,
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

router = APIRouter(prefix="/manage-guests", tags=["admin"])
db_session = Annotated[Session, Depends(get_db)]
logger = di_container.get_logger()


@router.get("/", response_class=HTMLResponse)
async def manage_guests(
    request: Request,
    current_admin: admin_dependency,
):
    """Serve the manage guests page."""
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    return templates.TemplateResponse(
        "admin/manage_guests.html",
        {
            "request": request,
            "admin": current_admin,
        },
    )


@router.get("/search")
async def search_guests(
    request: Request,
    db: db_session,
    current_admin: admin_dependency,
    guest_id: Optional[int] = None,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
) -> JSONResponse:
    """
    Search for guests by first name and/or last name.
    Returns a list of matching guests.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    try:
        find_guest: FindGuestUseCase = di_container.build_find_guest_use_case(db)
        logger.debug(
            f"Searching for guests with guest_id: {guest_id}, first_name: {first_name}, last_name: {last_name}"
        )
        # Search for guests
        guest: Union[Guest, None] = find_guest.execute(guest_id, first_name, last_name)

        if not guest:
            # Create a more detailed error message based on search criteria
            search_criteria = []
            if guest_id:
                search_criteria.append(f"ID: {guest_id}")
            if first_name:
                search_criteria.append(f"first name: '{first_name}'")
            if last_name:
                search_criteria.append(f"last name: '{last_name}'")

            criteria_str = ", ".join(search_criteria)
            error_message = f"No guests found matching the criteria: {criteria_str}"

            return JSONResponse(
                content={
                    "status": "error",
                    "message": error_message,
                    "search_criteria": {
                        "guest_id": guest_id,
                        "first_name": first_name,
                        "last_name": last_name,
                    },
                },
                status_code=404,
            )

        # Convert guest to dictionary only if it's not None
        guest_dict = guest.model_dump()

        # If the guest has a plus one, get the plus one's information
        if guest.has_guest and guest.guest_id:
            try:
                plus_one: Guest = find_guest.execute(guest_id=guest.guest_id)
                if plus_one:
                    guest_dict["plus_one"] = plus_one.model_dump()
                else:
                    guest_dict["plus_one"] = None
            except Exception as e:
                logger.error(f"Error finding plus one guest: {str(e)}")
                guest_dict["plus_one"] = None

        return JSONResponse(
            content={
                "status": "success",
                "guests": guest_dict,
            },
            status_code=200,
        )

    except Exception as e:
        logger.error(f"Error searching for guests: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"An error occurred while searching for guests: {str(e)}",
            },
            status_code=500,
        )


@router.get("/{guest_id}/edit", response_class=HTMLResponse)
async def edit_guest_page(
    request: Request,
    guest_id: int,
    db: db_session,
    current_admin: admin_dependency,
):
    """Serve the edit guest page."""
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    try:
        find_guest: FindGuestUseCase = di_container.build_find_guest_use_case(db)
        guest: Guest = find_guest.execute(guest_id=guest_id)

        # Get all menu choices from the enum
        menu_choices = [
            {"value": choice.value, "label": choice.value} for choice in MenuChoices
        ]

        # Check if the guest has a plus one
        if not guest.has_guest and not guest.guest_id:
            # Use the regular template if no plus one
            return templates.TemplateResponse(
                "admin/edit_guest.html",
                {
                    "request": request,
                    "admin": current_admin,
                    "guest": guest,
                    "menu_choices": menu_choices,
                },
            )

        plus_one: Guest = find_guest.execute(guest_id=guest.guest_id)
        logger.debug(f"Plus one guest found: {plus_one}")

        # Use the template with plus one
        return templates.TemplateResponse(
            "admin/edit_guest_with_plus_one.html",
            {
                "request": request,
                "admin": current_admin,
                "guest": guest,
                "plus_one": plus_one,
                "menu_choices": menu_choices,
            },
        )

    except Exception as e:
        logger.error(f"Error loading guest for editing: {str(e)}")
        return templates.TemplateResponse(
            "admin/edit_guest.html",
            {
                "request": request,
                "admin": current_admin,
                "error": "Failed to load guest",
            },
        )


@router.put("/{guest_id}/update", response_class=JSONResponse)
async def update_guest_by_id(
    request: Request,
    guest_id: int,
    current_admin: admin_dependency,
    db: db_session,
):
    """Update a guest by ID."""
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    try:
        # Get the guest data from the request body
        guest_data = await request.json()
        update_guest: UpdateGuestUseCase = di_container.build_update_guest_use_case(db)

        # Create a Guest object from the request data
        guest = Guest(
            id=guest_id,
            first_name=guest_data.get("first_name"),
            last_name=guest_data.get("last_name"),
            email=guest_data.get("email"),
            phone=guest_data.get("phone"),
            menu=guest_data.get("menu"),
            dietary_requirements=guest_data.get("dietary_requirements"),
            needs_hotel=guest_data.get("needs_hotel"),
            has_guest=guest_data.get("has_guest"),
            guest_id=guest_data.get("guest_id"),
        )

        updated_guest: Guest = update_guest.execute(guest)
        logger.debug(f"Guest updated: {updated_guest}")

        return JSONResponse(
            content={
                "status": "success",
                "message": "Guest updated successfully",
                "guest": updated_guest.id,
            },
            status_code=status.HTTP_204_NO_CONTENT,
        )
    except Exception as e:
        logger.error(f"Error updating guest: {str(e)}")
        return JSONResponse(
            content={
                "status": "error",
                "message": f"Failed to update guest: {str(e)}",
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/update/success", response_class=HTMLResponse)
async def update_success(
    request: Request,
    current_admin: admin_dependency,
):
    """Serve the update success page."""
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    return templates.TemplateResponse(
        "admin/update_success.html",
        {
            "request": request,
            "admin": current_admin,
        },
    )


@router.get("/update/failed", response_class=HTMLResponse)
async def update_failed(
    request: Request,
    current_admin: admin_dependency,
):
    """Serve the update failed page."""
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    return templates.TemplateResponse(
        "admin/update_failed.html",
        {
            "request": request,
            "admin": current_admin,
        },
    )
