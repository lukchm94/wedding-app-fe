from typing import Any, Dict, Optional, Union

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.orm import Session

from src.modules.guests.application.save_rsvp import (
    RSVPFormData,
    SavedGuests,
    SaveRSVPUseCase,
)
from src.modules.guests.domain.guest import Guest, GuestWithRsvpStatus
from src.shared.controllers.rsvp.form_input import FormInput
from src.shared.controllers.rsvp.search import RsvpFormData, SearchController
from src.shared.database.config import get_db
from src.shared.server.config import di_container, templates
from src.shared.utils.__validations import MenuChoices, RsvpStatus
from src.shared.utils.logger import logger

router = APIRouter(prefix="/rsvp", tags=["rsvp"])

# TODO: fix menu mapping to have the conversion in one place not in the router
MENU_MAPPING = {
    "meat": MenuChoices.MEAT,
    "vegetarian": MenuChoices.VEGETARIAN,
    "vegan": MenuChoices.VEGAN,
    "menu mięsne": MenuChoices.MEAT,
    "menu wegetariańskie": MenuChoices.VEGETARIAN,
    "menu wegańskie": MenuChoices.VEGAN,
}


def get_menu_choice(menu_value: str) -> str | None:
    if not menu_value:
        return None
    menu_value = menu_value.lower()

    try:
        return MenuChoices(menu_value).value
    except ValueError:
        return MENU_MAPPING.get(menu_value, MenuChoices.MEAT).value


@router.get("/", response_class=HTMLResponse)
async def rsvp_search(request: Request):
    """Landing page with search functionality."""
    return templates.TemplateResponse("rsvp_search.html", {"request": request})


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
    results: list[GuestWithRsvpStatus] | list[Guest] = search_controller.search(
        first_name, last_name
    )
    logger.info(f"Search results: {results}")
    return results


@router.get("/form/{guest_id}", response_class=HTMLResponse)
async def rsvp_form(  # type: ignore
    req: Request,
    guest_id: int,
    plus_one_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """Show RSVP form pre-filled with guest data or show submitted RSVP if already confirmed."""
    search_controller: SearchController = di_container.build_search_controller(db)
    process_rsvp_form: RsvpFormData = search_controller.process_rsvp_form(
        req, guest_id, plus_one_id
    )

    if not process_rsvp_form:
        return templates.TemplateResponse("rsvp_search.html", {"request": req})

    guest: Union[GuestWithRsvpStatus, None] = process_rsvp_form.get("guest")
    plus_one: Union[GuestWithRsvpStatus, None] = process_rsvp_form.get("plus_one")

    if guest and guest.rsvp_status == RsvpStatus.CONFIRMED.value:
        form_input: FormInput = FormInput(guest=guest, plus_one=plus_one)

        return templates.TemplateResponse(
            "rsvp_submitted.html",
            form_input.as_dict(req),
            status_code=status.HTTP_200_OK,
        )

    return templates.TemplateResponse("rsvp.html", process_rsvp_form)  # type: ignore


@router.post("/form/{guest_id}", response_class=HTMLResponse)
async def rsvp_submit(
    request: Request,
    guest_id: int,
    plus_one_id: Optional[int],
    firstName: str = Form(...),
    lastName: str = Form(...),
    menu: str = Form(...),
    dietaryRequirements: Optional[str] = Form(None),
    phone: str = Form(...),
    email: str = Form(...),
    needsHotel: bool = Form(...),
    hasGuest: Optional[bool] = Form(None),
    plusOneFirstName: Optional[str] = Form(None),
    plusOneLastName: Optional[str] = Form(None),
    plusOneMenu: Optional[str] = Form(None),
    plusOneDietaryRequirements: Optional[str] = Form(None),
    plusOnePhone: Optional[str] = Form(None),
    plusOneEmail: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    """
    Handle RSVP form submission for a specific guest.
    """
    try:
        save_rsvp_use_case: SaveRSVPUseCase = di_container.build_save_rsvp_use_case(db)

        menu_choice = get_menu_choice(menu)
        plus_one_menu_choice = get_menu_choice(plusOneMenu) if plusOneMenu else None

        rsvp_form: Dict[str, Any] = {
            "first_name": firstName,
            "last_name": lastName,
            "menu": menu_choice,
            "dietary_requirements": dietaryRequirements,
            "phone": phone,
            "email": email,
            "needs_hotel": needsHotel,
            "has_guest": hasGuest,
            "plus_one_first_name": plusOneFirstName,
            "plus_one_last_name": plusOneLastName,
            "plus_one_menu": plus_one_menu_choice,
            "plus_one_dietary_requirements": plusOneDietaryRequirements,
            "plus_one_phone": plusOnePhone,
            "plus_one_email": plusOneEmail,
        }

        rsvp_data = RSVPFormData(**rsvp_form)

        guests_saved: SavedGuests = save_rsvp_use_case.execute(
            rsvp_data, guest_id, plus_one_id
        )

        return templates.TemplateResponse(
            "rsvp_completed.html",
            {
                "request": request,
                "title": guests_saved.formatted_names,
                "message": guests_saved.message,
                "success": True,
            },
            status_code=status.HTTP_200_OK,
        )
    except Exception as e:
        logger.error(f"Error processing RSVP: {str(e)}")
        return templates.TemplateResponse(
            "home.html",
            {
                "request": request,
                "message": f"Wystąpił błąd podczas przetwarzania formularza: {str(e)}",
                "success": False,
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
