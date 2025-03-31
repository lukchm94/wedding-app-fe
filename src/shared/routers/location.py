import os
from pathlib import Path

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.shared.__settings import settings
from src.shared.server.config import templates

router = APIRouter(prefix="/location", tags=["location"])


@router.get("/", response_class=HTMLResponse)
async def location(request: Request):
    images_dir = Path("src/shared/static/images/maleszowa")
    images = sorted([f.name for f in images_dir.glob("*.png")])

    return templates.TemplateResponse(
        "location.html",
        {
            "request": request,
            "instagram_url": settings.PLACE_IG_LINK,
            "google_maps_url": settings.GOOGLE_MAPS_LINK,
            "image_rotation_time": settings.image_banner.IMAGE_ROTATION_TIME,
            "image_banner_height": settings.image_banner.IMAGE_BANNER_HEIGHT,
            "image_transition_duration": settings.image_banner.IMAGE_TRANSITION_DURATION,
            "image_banner_button_bg": settings.image_banner.IMAGE_BANNER_BUTTON_BG,
            "image_banner_button_hover_bg": settings.image_banner.IMAGE_BANNER_BUTTON_HOVER_BG,
            "image_banner_button_color": settings.image_banner.IMAGE_BANNER_BUTTON_COLOR,
            "image_banner_button_hover_color": settings.image_banner.IMAGE_BANNER_BUTTON_HOVER_COLOR,
            "images": images,
        },
    )
