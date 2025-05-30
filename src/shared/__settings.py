from pathlib import Path
from typing import Any, Dict

from pydantic_settings import BaseSettings


class TextSettings(BaseSettings):
    # Use project root relative paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    PATH: str = str(PROJECT_ROOT / "src/shared/static/text")
    ITINERARY_FILE: str = "itinerary.json"
    FULL_PATH: str = str(PROJECT_ROOT / "src/shared/static/text/itinerary.json")
    ITINERARY_KEY: str = "itinerary"

    class Config:
        env_prefix = "TEXT_"


class ImageSettings(BaseSettings):
    PATH: str = "src/shared/static/images/"


class IconsSettings(BaseSettings):
    PATH: str = "src/shared/static/icons/"


class ImageBannerSettings(BaseSettings):
    IMAGE_ROTATION_TIME: int = 10
    IMAGE_BANNER_HEIGHT: int = 400
    IMAGE_TRANSITION_DURATION: int = 5
    IMAGE_BANNER_BUTTON_BG: str = "rgba(255, 255, 255, 0.7)"
    IMAGE_BANNER_BUTTON_HOVER_BG: str = "rgba(255, 255, 255, 0.9)"
    IMAGE_BANNER_BUTTON_COLOR: str = "#4B5563"
    IMAGE_BANNER_BUTTON_HOVER_COLOR: str = "#1D4ED8"


class Settings(BaseSettings):
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"

    # Database
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SERVER: str
    MYSQL_PORT: str = "3380"
    MYSQL_DB: str
    DATABASE_URL: str | None = None

    # Image Banner Settings
    image_banner: ImageBannerSettings = ImageBannerSettings()
    # Text Settings
    text: TextSettings = TextSettings()
    # Image Settings
    image: ImageSettings = ImageSettings()
    # Icons Settings
    icons: IconsSettings = IconsSettings()

    # URLs
    PLACE_IG_LINK: str
    GOOGLE_MAPS_LINK: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env file

    def __init__(self, **kwargs: Dict[str, Any]):
        super().__init__(**kwargs)  # type: ignore
        if not self.DATABASE_URL:
            self.DATABASE_URL = f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"  # type: ignore


settings = Settings()
