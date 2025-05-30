from fastapi import APIRouter

from .admin import router as admin_routers
from .health import router as health_router
from .home import router as home_router
from .itinerary import router as itinerary_router
from .location import router as location_router
from .login import router as login_router
from .rsvp import router as rsvp_router
from .users import router as users_router

router = APIRouter()


router.include_router(health_router)
router.include_router(home_router)
router.include_router(location_router)
router.include_router(rsvp_router)
router.include_router(users_router)
router.include_router(admin_routers)
router.include_router(login_router)
router.include_router(itinerary_router)
