from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.shared.auth.authenticate import admin_dependency
from src.shared.database.config import get_db
from src.shared.server.config import templates

router = APIRouter(prefix="/set-schedule", tags=["admin"])
db_session = Annotated[Session, Depends(get_db)]


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    current_admin: admin_dependency,
):
    """
    Serve the admin dashboard page.
    Only accessible to authenticated admin users.
    """
    # If current_admin is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
            "admin": current_admin,
        },
    )
