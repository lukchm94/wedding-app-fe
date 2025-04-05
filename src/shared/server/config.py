from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from src.shared.DIContaner.container import DIContainer

# Templates
templates = Jinja2Templates(directory="src/shared/templates")

# Static files
static = StaticFiles(directory="src/shared/static")

# Initialize DI container
di_container = DIContainer()
