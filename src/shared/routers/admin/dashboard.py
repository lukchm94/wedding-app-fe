from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.shared.server.config import templates  # Ensure the correct import path

router = APIRouter(prefix="/dashboard", tags=["admin"])


@router.get("/", response_class=HTMLResponse)
async def admin_dashboard(request: Request):
    """
    Serve the admin dashboard page.
    """
    return templates.TemplateResponse(
        "admin/dashboard.html",
        {
            "request": request,
        },
    )
