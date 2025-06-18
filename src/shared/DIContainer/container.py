from typing import Any, Dict, TypeVar

from sqlalchemy.orm import Session

from src.modules.guests.application.create_guest.create_guest_use_case import (
    CreateGuestUseCase,
)
from src.modules.guests.application.find_guest.find_guest_use_case import (
    FindGuestUseCase,
)
from src.modules.guests.application.save_rsvp.save_rsvp_use_case import SaveRSVPUseCase
from src.modules.guests.application.update_guest.update_guest_use_case import (
    UpdateGuestUseCase,
)
from src.modules.guests.domain.repository import GuestRepository
from src.modules.guests.domain.service import GuestService
from src.modules.guests.infra.repository.implementation import GuestRepoImpl
from src.modules.itinerary.application.use_case.show_active_itinerary import (
    ShowActiveItineraryUseCase,
)
from src.modules.itinerary.application.use_case.upload_itinerary import (
    UploadItineraryUseCase,
)
from src.modules.itinerary.domain.itinerary_service import ItineraryService
from src.modules.itinerary.infrastructure.repository.os.os_itinerary_impl import (
    OsItineraryRepositoryImplementation,
    OsPaths,
)
from src.modules.users.application.login.login_use_case import LoginUseCase
from src.modules.users.domain.password_service import PasswordService
from src.modules.users.domain.token_service import TokenService
from src.modules.users.domain.user_service import UserService
from src.modules.users.infra.repository.user_repo_impl import UserRepoImpl
from src.shared.controllers.admin.add_guests import GuestController
from src.shared.controllers.admin.update_itinerary import ItineraryController
from src.shared.controllers.itinerary.get_elements import ItineraryGetElementsController
from src.shared.controllers.rsvp.search import SearchController
from src.shared.database.config import SessionLocal
from src.shared.templates.paths import HtmlPaths
from src.shared.utils.logger import Logger, get_logger

from .registered_services import RegisteredServices

T = TypeVar("T")


class DIContainer:
    """
    Dependency Injection Container
    """

    def __init__(self):
        self._services: Dict[str, Any] = {}

        # Initialize logger
        self._logger: Logger = get_logger()
        self._logger.debug("DIContainer initialized")

        # Initialize database connection
        self.register(RegisteredServices.DB_SESSION.value, SessionLocal)

        # Initialize domain services
        self.register(
            RegisteredServices.PASSWORD_SERVICE.value, PasswordService(self._logger)
        )

        self.register(
            RegisteredServices.TOKEN_SERVICE.value, TokenService(self._logger)
        )
        self.register(
            RegisteredServices.GUEST_CONTROLLER.value, GuestController(self._logger)
        )
        self.register(RegisteredServices.HTML_PATHS.value, HtmlPaths())
        self.register(RegisteredServices.SETTINGS.value, self._logger)
        self.register(
            RegisteredServices.OS_PATHS.value,
            OsPaths(self.get(RegisteredServices.SETTINGS.value)),
        )

        self.register(
            RegisteredServices.ITINERARY_REPO_IMPL.value,
            OsItineraryRepositoryImplementation(
                self._logger, self.get(RegisteredServices.OS_PATHS.value)
            ),
        )
        self.register(
            RegisteredServices.ITINERARY_SERVICE.value,
            ItineraryService(
                self.get(RegisteredServices.ITINERARY_REPO_IMPL.value), self._logger
            ),
        )

        self.register(
            RegisteredServices.SHOW_ACTIVE_USE_CASE.value,
            ShowActiveItineraryUseCase(
                self.get(RegisteredServices.ITINERARY_SERVICE.value),
                self._logger,
            ),
        )

        self.register(
            RegisteredServices.UPLOAD_ITINERARY_USE_CASE.value,
            UploadItineraryUseCase(
                self.get(RegisteredServices.ITINERARY_SERVICE.value), self._logger
            ),
        )
        self.register(
            RegisteredServices.ITINERARY_CONTROLLER.value,
            ItineraryController(
                self._logger,
                self.get(RegisteredServices.UPLOAD_ITINERARY_USE_CASE.value),
                self.get(RegisteredServices.SHOW_ACTIVE_USE_CASE.value),
            ),
        )

    def register(self, name: str, service: Any) -> None:
        """
        Register a service in the container
        """
        self._services[name] = service

    def get(self, name: str) -> Any:
        """
        Get a service from the container
        """
        return self._services.get(name)

    def build_user_repo(self, db: Session) -> UserRepoImpl:
        """
        Build the user repository
        """
        user_repo_impl = UserRepoImpl(db, self._logger)
        return user_repo_impl

    def build_guest_repo(self, db: Session) -> GuestRepository:
        """
        Build the guest repository
        """
        guest_repo_impl = GuestRepoImpl(db, self._logger)
        return guest_repo_impl

    def build_guest_service(self, db: Session) -> GuestService:
        guest_repo = GuestRepoImpl(db, self._logger)
        guest_service = GuestService(guest_repo)
        return guest_service

    def build_login_use_case(self, db: Session) -> LoginUseCase:
        """
        Build the login use case
        """
        user_repo: UserRepoImpl = self.build_user_repo(db)
        user_service: UserService = UserService(self._logger, user_repo)
        login_use_case: LoginUseCase = LoginUseCase(
            user_service=user_service,
            password_service=self.get(RegisteredServices.PASSWORD_SERVICE.value),
            jwt_service=self.get(RegisteredServices.TOKEN_SERVICE.value),
            logger=self._logger,
        )
        return login_use_case

    def build_create_guest_use_case(self, db: Session) -> CreateGuestUseCase:
        """
        Build the create guest use case
        """
        guest_service: GuestService = self.build_guest_service(db)
        create_guest_use_case: CreateGuestUseCase = CreateGuestUseCase(
            guest_service=guest_service, logger=self._logger
        )
        return create_guest_use_case

    def build_update_guest_use_case(self, db: Session) -> UpdateGuestUseCase:
        """
        Build the update guest use case
        """
        guest_service: GuestService = self.build_guest_service(db)
        update_guest_use_case: UpdateGuestUseCase = UpdateGuestUseCase(
            guest_service=guest_service, logger=self._logger
        )
        return update_guest_use_case

    def get_logger(self) -> Logger:
        """
        Get the logger
        """
        return self._logger

    def build_guest_controller(self) -> GuestController:
        """
        Build the guest controller
        """
        return GuestController(self._logger)

    def build_find_guest_use_case(self, db: Session) -> FindGuestUseCase:
        """
        Build the find guest use case
        """
        guest_service: GuestService = self.build_guest_service(db)
        find_guest_use_case: FindGuestUseCase = FindGuestUseCase(
            guest_service=guest_service
        )
        return find_guest_use_case

    def build_search_controller(self, db: Session) -> SearchController:
        """
        Build the search controller
        """
        find_guest_use_case: FindGuestUseCase = self.build_find_guest_use_case(db)
        return SearchController(
            db=db,
            find_guest_use_case=find_guest_use_case,
            logger=self._logger,
        )

    def build_save_rsvp_use_case(self, db: Session) -> SaveRSVPUseCase:
        guest_service: GuestService = self.build_guest_service(db)
        save_rsvp_use_case: SaveRSVPUseCase = SaveRSVPUseCase(
            logger=self._logger, guest_service=guest_service
        )
        return save_rsvp_use_case

    def build_itinerary_get_elements_controller(self) -> ItineraryGetElementsController:
        """
        Build the itinerary get elements controller
        """
        return ItineraryGetElementsController(self._logger)
