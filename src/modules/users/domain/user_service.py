from logging import Logger

from ..infra.repository.user_repo_impl import UserRepoImpl
from .user_model import UserModel
from .user_repository import UserRepository


class UserService:
    def __init__(self, logger: Logger, user_repo: UserRepoImpl) -> None:
        self.logger: Logger = logger
        self.user_repo: UserRepoImpl = user_repo

    def find_by_email(self, email: str) -> UserModel:
        # This method should be implemented to find a user by email
        self.logger.debug(f"Finding user by email: {email}")
        return self.user_repo.get_user_by_email(email)

    def create_user(self, user: UserModel) -> UserModel:
        # This method should be implemented to create a new user
        self.logger.debug(f"Creating user: {user}")
        return self.user_repo.create_user(user)
