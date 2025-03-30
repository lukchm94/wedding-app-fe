from .health import router as health_router
from .home import router as home_router
from .location import router as location_router

all_routers = [health_router, home_router, location_router]
