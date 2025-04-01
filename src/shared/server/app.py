from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from src.shared.database.init import lifespan
from src.shared.routers import router
from src.shared.routers.admin.dashboard import router as admin_dashboard_router
from src.shared.server.config import static, templates

app = FastAPI(lifespan=lifespan)

# Mount static files
app.mount("/static", static, name="static")

# Include routers
app.include_router(router)
app.include_router(admin_dashboard_router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    if "admin" in request.url.path:
        return templates.TemplateResponse(
            "admin/404.html", {"request": request}, status_code=404
        )
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
