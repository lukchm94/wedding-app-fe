from typing import Optional

from fastapi import APIRouter, Form, Request
from fastapi.responses import HTMLResponse

from src.shared.server.config import templates

router = APIRouter(prefix="/rsvp", tags=["rsvp"])


@router.get("/", response_class=HTMLResponse)
async def rsvp_form(request: Request):
    return templates.TemplateResponse("rsvp.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def rsvp_submit(
    request: Request,
    firstName: str = Form(...),
    lastName: str = Form(...),
    hasGuest: str = Form(...),
    guestName: Optional[str] = Form(None),
    menu: str = Form(...),
    dietaryRequirements: Optional[str] = Form(None),
    needsHotel: str = Form(...),
    phone: str = Form(...),
    email: str = Form(...),
):
    # Here you can add logic to save the RSVP data
    # For now, we'll just return a success message
    return templates.TemplateResponse(
        "rsvp_completed.html",
        {
            "request": request,
            "message": "Dziękujemy za potwierdzenie obecności!",
            "success": True,
        },
    )
