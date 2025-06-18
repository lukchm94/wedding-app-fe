from logging import Logger
from typing import Annotated

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from sqlalchemy.orm import Session

from src.shared.auth.authenticate import admin_dependency
from src.shared.controllers.admin.update_itinerary import (
    ItineraryController,
    SchedulePayload,
)
from src.shared.database.config import get_db
from src.shared.server.config import di_container, templates
from src.shared.templates.paths import HtmlPaths

router = APIRouter(prefix="/set-schedule", tags=["admin"])
db_session = Annotated[Session, Depends(get_db)]
HTML_TEMPLATES: HtmlPaths = di_container.get("html_paths")
logger: Logger = di_container.get_logger()


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
        HTML_TEMPLATES.ADMIN.SCHEDULE,
        {
            "request": request,
            "admin": current_admin,
        },
    )


@router.post("/", response_class=JSONResponse)
async def save_itinerary(current_admin: admin_dependency, payload: SchedulePayload):
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    logger.info(
        f"[{HTML_TEMPLATES.ADMIN.SCHEDULE}] - Received payload: {payload.model_dump()}"
    )
    itinerary_controller: ItineraryController = di_container.get("itinerary_controller")
    try:
        itinerary_controller.upload(payload)

        return JSONResponse(
            {
                "status": "success",
                "message": "Schedule saved successfully",
                "data": payload.model_dump(),
            },
            status_code=status.HTTP_201_CREATED,
        )
    except Exception as err:
        logger.error(f"Error saving itinerary: {err}")
        return JSONResponse(
            {
                "status": "error",
                "message": str(err),
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


@router.get("/success", response_class=HTMLResponse)
async def success_page(
    request: Request,
    current_admin: admin_dependency,
):
    """Serve the success page after saving the schedule."""
    if isinstance(current_admin, RedirectResponse):
        return current_admin

    return templates.TemplateResponse(
        HTML_TEMPLATES.ADMIN.OK,
        {
            "request": request,
            "admin": current_admin,
            "itinerary": [
                "Schedule updated successfully!"
            ],  # You can pass the saved schedule here if needed
        },
    )
