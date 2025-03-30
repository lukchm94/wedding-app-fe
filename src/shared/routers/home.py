from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.shared.server.config import templates

router = APIRouter()

WEDDING_DATE: datetime = datetime(2026, 6, 26, 16, 0, 0)


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    now: datetime = datetime.now()

    # Calculate time difference
    time_diff = WEDDING_DATE - now

    # Calculate days, hours, minutes, and seconds
    days: int = time_diff.days
    hours: int = time_diff.seconds // 3600
    minutes: int = (time_diff.seconds % 3600) // 60
    seconds: int = time_diff.seconds % 60

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "days": days,
            "hours": hours,
            "minutes": minutes,
            "seconds": seconds,
            "wedding_date": WEDDING_DATE.strftime("%Y-%m-%dT%H:%M:%S"),
        },
    )
