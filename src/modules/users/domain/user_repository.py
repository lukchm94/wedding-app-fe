from abc import ABC, abstractmethod
from typing import Optional

from .user_model import UserModel


class UserRepository(ABC):
    """Abstract base class for user repository."""

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> Optional[UserModel]:
        """Retrieve a user by ID."""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> Optional[UserModel]:
        """Retrieve a user by email."""
        pass

    @abstractmethod
    def create_user(self, user: UserModel) -> UserModel:
        """Create a new user."""
        pass

    @abstractmethod
    def update_user(self, user: UserModel) -> UserModel:
        """Update an existing user."""
        pass

    @abstractmethod
    def delete_user(self, user_id: int) -> None:
        """Delete a user by ID."""
        pass
