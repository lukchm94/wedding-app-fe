import json
from typing import List, Optional, Union

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.modules.guests.application.find_guest.find_guest_use_case import (
    FindGuestUseCase,
)
from src.modules.guests.domain.guest import Guest
from src.modules.guests.domain.service import GuestService
from src.modules.guests.infra.repository.implementation import GuestRepoImpl
from src.shared.controllers.rsvp.search import SearchController
from src.shared.database.config import get_db
from src.shared.database.models.guest import Guest as GuestModel
from src.shared.server.config import di_container, templates
from src.shared.utils.__validations import MenuChoices
from src.shared.utils.logger import logger

router = APIRouter(prefix="/rsvp", tags=["rsvp"])


@router.get("/", response_class=HTMLResponse)
async def rsvp_search(request: Request):
    """Landing page with search functionality."""
    logger.info(f"rsvp_search")
    return templates.TemplateResponse("rsvp_search.html", {"request": request})


@router.get("/form/{guest_id}", response_class=HTMLResponse)
async def rsvp_form(
    request: Request,
    guest_id: int,
    plus_one_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Show RSVP form pre-filled with guest data."""
    search_controller: SearchController = di_container.build_search_controller(db)
    process_rsvp_form: dict = search_controller.process_rsvp_form(
        request, guest_id, plus_one_id
    )
    logger.info(f"process_rsvp_form: {process_rsvp_form}")
    return templates.TemplateResponse(
        "rsvp.html",
        process_rsvp_form,
    )


@router.get("/search", response_class=JSONResponse)
async def search_guests(
    first_name: str,
    last_name: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """
    Search for guests by first name and optionally last name.
    Returns a list of matching guests.
    """
    search_controller: SearchController = di_container.build_search_controller(db)
    results: list[Guest] = search_controller.search(first_name, last_name)
    logger.info(f"Search results: {results}")
    return results


@router.post("/form/{guest_id}", response_class=HTMLResponse)
async def rsvp_submit(
    request: Request,
    guest_id: int,
    hasGuest: str = Form(...),
    menu: str = Form(...),
    dietaryRequirements: Optional[str] = Form(None),
    needsHotel: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
    db: Session = Depends(get_db),
):
    """
    Handle RSVP form submission for a specific guest.
    """
    try:
        guest_repo = GuestRepoImpl(db, logger)
        guest_service = GuestService(guest_repo)
        find_guest_use_case = FindGuestUseCase(guest_service)

        existing_guest = find_guest_use_case.execute(guest_id=guest_id)
        if not existing_guest:
            raise HTTPException(status_code=404, detail="Guest not found")

        # Update guest information
        existing_guest.has_guest = hasGuest == "yes"
        existing_guest.menu = MenuChoices(menu)
        existing_guest.dietary_requirements = dietaryRequirements
        existing_guest.needs_hotel = needsHotel == "yes"
        existing_guest.phone = phone
        existing_guest.email = email

        # Update the guest in the database
        updated_guest = guest_service.update_guest(existing_guest)

        # Update RSVP status
        guest_model = db.query(GuestModel).filter(GuestModel.id == guest_id).first()
        if guest_model:
            guest_model.rsvp_status = "confirmed"
            db.commit()

        logger.info(f"Updated guest RSVP: {updated_guest}")

        return templates.TemplateResponse(
            "rsvp_completed.html",
            {
                "request": request,
                "message": "Dziękujemy za potwierdzenie obecności!",
                "success": True,
            },
        )
    except Exception as e:
        logger.error(f"Error processing RSVP: {str(e)}")
        return templates.TemplateResponse(
            "rsvp.html",
            {
                "request": request,
                "guest": existing_guest if "existing_guest" in locals() else None,
                "message": f"Wystąpił błąd podczas przetwarzania formularza: {str(e)}",
                "success": False,
            },
        )
