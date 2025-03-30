from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse

from src.shared.routers import all_routers
from src.shared.server.config import static, templates

app = FastAPI()

# Mount static files
app.mount("/static", static, name="static")

# Include routers
for router in all_routers:
    app.include_router(router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc):
    return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
