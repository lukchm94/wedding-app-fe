from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from ..auth.email_authentication import authenticate_admin
from ..database.config import get_db
from ..server.config import templates

router = APIRouter(prefix="/login", tags=["login"])
db_session = Annotated[Session, Depends(get_db)]


@router.get("/", response_class=HTMLResponse)
async def login_page(request: Request):
    """
    Serve the login page.
    """
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
        },
    )


@router.post("/")
async def login(
    request: Request,
    db: db_session,
    email: Annotated[str, Form(...)],  # Extract email from form data
):
    """
    Handle login form submission.
    """
    try:
        # Authenticate the user
        authenticate_admin(email, db)
    except HTTPException as e:
        # Render the login page with an error message if authentication fails
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": e.detail,
            },
            status_code=e.status_code,
        )

    # Redirect to the admin dashboard after successful login
    return RedirectResponse(url="/admin/dashboard", status_code=303)
