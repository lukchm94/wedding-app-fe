from logging import Logger

from .user_model import UserModel


class UserService:
    def __init__(self, logger: Logger):
        self.logger: Logger = logger

    def find_by_email(self, email: str) -> UserModel:
        # This method should be implemented to find a user by email
        self.logger.debug(f"Finding user by email: {email}")
        pass
