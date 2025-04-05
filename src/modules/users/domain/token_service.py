from datetime import datetime, timedelta
from logging import Logger
from typing import Optional

from jose import jwt

from ....shared.__app_configs import TokenConfigs, TokenTypes
from ....shared.__settings import settings
from .user_model import UserModel, UserWithToken


class TokenService:
    expire_minutes: int
    logger: Logger

    def __init__(
        self,
        logger: Logger,
        expire_minutes: Optional[int] = None,
    ) -> None:
        self.expire_minutes: int = (
            expire_minutes
            if expire_minutes is not None
            else TokenConfigs.default_expiration.value
        )
        self.logger: Logger = logger
        self.logger.debug(
            f"TokenService initialized with expire_minutes: {self.expire_minutes}"
        )

    def generate_token(self, user: UserModel) -> UserWithToken:
        token: str = self._get_access_token(user)
        user_with_token: UserWithToken = UserWithToken(
            access_token=token, token_type=TokenTypes.bearer.value, user=user
        )
        self.logger.debug(f"Generated token for user: {user.username}")
        return user_with_token

    def _get_delta(self) -> timedelta:
        return timedelta(minutes=self.expire_minutes)

    def _get_access_token(self, user: UserModel) -> str:
        encode: dict = {
            "sub": user.username,
            "role": user.role,
        }
        expires: datetime = datetime.now() + self._get_delta()
        encode.update({"exp": expires})
        return jwt.encode(
            claims=encode,
            key=settings.SECRET_KEY,
            algorithm=TokenConfigs.algorithm.value,
        )
