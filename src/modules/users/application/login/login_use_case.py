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
    ):
        self.user_service: UserService = user_service
        self.password_service: PasswordService = password_service
        self.jwt_service: TokenService = jwt_service

    def execute(self, email: str, password: str) -> UserWithToken:
        user: UserModel = self.user_service.find_by_email(email)
        if not user:
            raise Exception("User not found")

        if not self.password_service.verify_password(password, user):
            raise Exception("Invalid password")

        token = self.jwt_service.generate_token(user)
        return token
