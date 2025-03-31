from fastapi import APIRouter

from .dashboard import router as dashboard_router
from .manage_guests import router as manage_guests_router

router = APIRouter(prefix="/admin", tags=["admin"])

router.include_router(manage_guests_router)
router.include_router(dashboard_router)
