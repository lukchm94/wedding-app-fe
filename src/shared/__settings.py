from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-this-in-production"

    # Image Banner Settings
    IMAGE_ROTATION_TIME: int = 5
    IMAGE_BANNER_HEIGHT: int = 400
    IMAGE_TRANSITION_DURATION: int = 1
    IMAGE_BANNER_BUTTON_BG: str = "rgba(255, 255, 255, 0.7)"
    IMAGE_BANNER_BUTTON_HOVER_BG: str = "rgba(255, 255, 255, 0.9)"
    IMAGE_BANNER_BUTTON_COLOR: str = "#4B5563"
    IMAGE_BANNER_BUTTON_HOVER_COLOR: str = "#1D4ED8"

    # URLs
    PLACE_IG_LINK: str
    GOOGLE_MAPS_LINK: str

    class Config:
        env_file = ".env"
        extra = "allow"  # Allow extra fields from .env file


settings = Settings()
