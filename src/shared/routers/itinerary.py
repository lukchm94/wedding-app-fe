from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from src.shared.server.config import templates

from ..controllers.itinerary.get_elements import ItineraryGetElementsController
from ..controllers.itinerary.models.itinerary import ItineraryElement
from ..server.config import di_container

router = APIRouter(prefix="/plan-wesela", tags=["plan-wesela"])


@router.get("/", response_class=HTMLResponse)
async def itinerary(request: Request):
    controller: ItineraryGetElementsController = (
        di_container.build_itinerary_get_elements_controller()
    )
    elements: list[ItineraryElement] = controller.read_from_file()
    return templates.TemplateResponse(
        "plan-wesela.html",
        {
            "request": request,
            "items": [e.model_dump() for e in elements],
        },
    )
