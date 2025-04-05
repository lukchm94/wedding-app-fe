from typing import Annotated

from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.shared.server.config import di_container

from ...modules.users.application.login.login_use_case import LoginUseCase
from ...modules.users.domain.user_model import UserWithToken
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
    email: Annotated[str, Form(...)],  # Extract email from form data
    password: Annotated[str, Form(...)],  # Extract password from form data
    db: db_session,
):
    """
    Handle login form submission.
    """
    try:
        # Create a login use case with the current database session
        login_use_case: LoginUseCase = di_container.build_login_use_case(db)
        # Authenticate the user using the login_use_case
        result: UserWithToken = login_use_case.execute(email=email, password=password)

        # Create a response with the token in a cookie
        response = RedirectResponse(url="/admin/dashboard", status_code=303)
        response.set_cookie(
            key="access_token",
            value=f"Bearer {result.access_token}",
            httponly=True,
            max_age=1800,  # 30 minutes
            path="/",
        )
        return response
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
    except Exception as e:
        # Handle other exceptions
        return templates.TemplateResponse(
            "login.html",
            {
                "request": request,
                "error": str(e),
            },
            status_code=500,
        )
