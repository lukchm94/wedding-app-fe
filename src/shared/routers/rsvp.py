from typing import List, Optional

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.modules.guests.application.find_guest.find_guest_use_case import (
    FindGuestUseCase,
)
from src.modules.guests.domain.guest import Guest
from src.modules.guests.domain.service import GuestService
from src.modules.guests.infra.repository.implementation import GuestRepoImpl
from src.shared.database.config import get_db
from src.shared.database.models.guest import Guest as GuestModel
from src.shared.server.config import templates
from src.shared.utils.__validations import MenuChoices
from src.shared.utils.logger import logger

router = APIRouter(prefix="/rsvp", tags=["rsvp"])


@router.get("/", response_class=HTMLResponse)
async def rsvp_search(request: Request):
    """Landing page with search functionality."""
    print("rsvp_search")
    return templates.TemplateResponse("rsvp_search.html", {"request": request})


@router.get("/form/{guest_id}", response_class=HTMLResponse)
async def rsvp_form(request: Request, guest_id: int, db: Session = Depends(get_db)):
    """Show RSVP form pre-filled with guest data."""
    guest_repo = GuestRepoImpl(db, logger)
    print(f"rsvp_form {guest_id}")
    guest_service = GuestService(guest_repo)
    find_guest_use_case = FindGuestUseCase(guest_service)
    print(f"find_guest_use_case {find_guest_use_case}")

    guest = find_guest_use_case.execute(guest_id=guest_id)
    print(f"guest {guest}")
    if not guest:
        return RedirectResponse(url="/rsvp", status_code=302)

    return templates.TemplateResponse(
        "rsvp.html",
        {
            "request": request,
            "guest": guest,
        },
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
    guest_repo = GuestRepoImpl(db, logger)
    guest_service = GuestService(guest_repo)
    find_guest_use_case = FindGuestUseCase(guest_service)

    # If only first name is provided, search for partial matches
    if last_name is None:
        # This is a simplified search - in a real app, you'd want to use a more sophisticated search
        # that handles partial matches in the database
        guests = (
            db.query(GuestModel)
            .filter(GuestModel.first_name.ilike(f"%{first_name}%"))
            .all()
        )
        return [
            {"id": g.id, "first_name": g.first_name, "last_name": g.last_name}
            for g in guests
        ]

    # If both first and last name are provided, search for exact matches
    guest = find_guest_use_case.execute(first_name=first_name, last_name=last_name)
    if guest:
        return [
            {
                "id": guest.id,
                "first_name": guest.first_name,
                "last_name": guest.last_name,
            }
        ]
    return []


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
