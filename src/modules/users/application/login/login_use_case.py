from logging import Logger
from typing import Union

from fastapi import HTTPException

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
        try:
            user: Union[UserModel, None] = self.user_service.find_by_email(email)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")

            if not self.password_service.verify_password(password, user):
                raise HTTPException(status_code=401, detail="Invalid password")

            token: UserWithToken = self.jwt_service.generate_token(user)
            return token
        except HTTPException:
            self.logger.error(f"Error in login use case: {e}")
            raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")
        except Exception as e:
            self.logger.error(f"Error in login use case: {e}")
            raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")
