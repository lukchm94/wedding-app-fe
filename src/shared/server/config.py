from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Templates
templates = Jinja2Templates(directory="src/shared/templates")

# Static files
static = StaticFiles(directory="src/shared/static")
