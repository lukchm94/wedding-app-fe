from fastapi import APIRouter

from .add_guests import router as add_guests_router
from .dashboard import router as dashboard_router
from .manage_guests import router as manage_guests_router
from .set_schedule import router as set_schedule_router

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(add_guests_router)
router.include_router(dashboard_router)
router.include_router(manage_guests_router)
router.include_router(set_schedule_router)
