from .health import router as health_router
from .home import router as home_router
from .location import router as location_router
from .rsvp import router as rsvp_router
from .test_db import router as test_router

all_routers = [health_router, home_router, location_router, rsvp_router, test_router]
