from enum import Enum


class RegisteredServices(str, Enum):
    """
    Enum for registered services in the DI container.
    """

    # Core services
    DB_SESSION = "db_session"
    LOGGER = "logger"
    PASSWORD_SERVICE = "password_service"
    TOKEN_SERVICE = "token_service"
    GUEST_CONTROLLER = "guest_controller"
    ITINERARY_CONTROLLER = "itinerary_controller"
    HTML_PATHS = "html_paths"
    SETTINGS = "settings"
    ITINERARY_REPO_IMPL = "itinerary_repo_impl"
    ITINERARY_SERVICE = "itinerary_service"
    SHOW_ACTIVE_USE_CASE = "show_active_use_case"
    UPLOAD_ITINERARY_USE_CASE = "upload_itinerary_use_case"
    OS_PATHS = "os_paths"
