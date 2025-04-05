from logging import Logger

from ...domain.password_service import PasswordService
from ...domain.token_service import TokenService
from ...domain.user_model import UserModel, UserWithToken
from ...domain.user_service import UserService


class LoginUseCase:
    def __init__(
        self,
        user_service: UserService,
        password_service: PasswordService,
        jwt_service: TokenService,
        logger: Logger,
    ):
        self.user_service: UserService = user_service
        self.password_service: PasswordService = password_service
        self.jwt_service: TokenService = jwt_service
        self.logger: Logger = logger

    def execute(self, email: str, password: str) -> UserWithToken:
        self.logger.debug("Executing login use case")
        self.logger.debug(f"Email: {email}")
        self.logger.debug(f"Password: {password}")
        user: UserModel = self.user_service.find_by_email(email)
        if not user:
            raise Exception("User not found")

        if not self.password_service.verify_password(password, user):
            raise Exception("Invalid password")

        token = self.jwt_service.generate_token(user)
        return token
