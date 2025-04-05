from sqlalchemy.orm import Session

from src.modules.guests.application.create_guest.create_guest_use_case import (
    CreateGuestUseCase,
)
from src.modules.guests.domain.repository import GuestRepository
from src.modules.guests.domain.service import GuestService
from src.modules.guests.infra.repository.implementation import GuestRepoImpl
from src.modules.users.application.login.login_use_case import LoginUseCase
from src.modules.users.domain.password_service import PasswordService
from src.modules.users.domain.token_service import TokenService
from src.modules.users.domain.user_repository import UserRepository
from src.modules.users.domain.user_service import UserService
from src.modules.users.infra.repository.user_repo_impl import UserRepoImpl
from src.shared.database.config import get_db
from src.shared.utils.logger import Logger, get_logger


class DIContainer:
    """
    Dependency Injection Container
    """

    def __init__(self):
        self._services = {}

        # Initialize logger
        self._logger: Logger = get_logger()
        self._logger.debug("DIContainer initialized")

        # Initialize database connection
        self.register("db", get_db())

        # Initialize repositories
        self.register("user_repo_impl", UserRepoImpl(self.get("db"), self._logger))
        self.register("guest_repo_impl", GuestRepoImpl(self.get("db"), self._logger))

        # Initialize domain services
        self.register(
            "user_service", UserService(self._logger, self.get("user_repo_impl"))
        )
        self.register("guest_service", GuestService(self.get("guest_repo_impl")))
        self.register("password_service", PasswordService(self._logger))
        self.register("token_service", TokenService(self._logger))

        # Initialize use cases
        self.register(
            "login_use_case",
            LoginUseCase(
                user_service=self.get("user_service"),
                password_service=self.get("password_service"),
                jwt_service=self.get("token_service"),
                logger=self._logger,
            ),
        )
        self.register(
            "create_guest_use_case",
            CreateGuestUseCase(
                guest_service=self.get("guest_service"), logger=self._logger
            ),
        ),

    def register(self, name, service):
        """
        Register a service in the container
        """
        self._services[name] = service

    def get(self, name):
        """
        Get a service from the container
        """
        return self._services.get(name)

    def build_user_repo(self, db: Session) -> UserRepository:
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

    def build_login_use_case(self, db: Session) -> LoginUseCase:
        """
        Build the login use case
        """
        user_repo: UserRepoImpl = self.build_user_repo(db)
        user_service: UserService = UserService(self._logger, user_repo)
        login_use_case: LoginUseCase = LoginUseCase(
            user_service=user_service,
            password_service=self.get("password_service"),
            jwt_service=self.get("token_service"),
            logger=self._logger,
        )
        return login_use_case

    def build_create_guest_use_case(self, db: Session) -> CreateGuestUseCase:
        """
        Build the create guest use case
        """
        guest_repo: GuestRepoImpl = self.build_guest_repo(db)
        guest_service: GuestService = GuestService(guest_repo)
        create_guest_use_case: CreateGuestUseCase = CreateGuestUseCase(
            guest_service=guest_service, logger=self._logger
        )
        return create_guest_use_case
