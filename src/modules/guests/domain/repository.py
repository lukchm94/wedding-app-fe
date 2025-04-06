from abc import ABC, abstractmethod
from typing import Optional

from .guest import Guest


class GuestRepository(ABC):
    @abstractmethod
    def get_guest_by_id(self, guest_id: int) -> Optional[Guest]:
        """Retrieve a guest by ID."""
        pass

    @abstractmethod
    def find_guest_by_name(self, first_name: str, last_name: str) -> Optional[Guest]:
        """Find a guest by first and last name."""
        pass

    @abstractmethod
    def create_guest(self, guest: Guest) -> Guest:
        """Create a new guest."""
        pass

    @abstractmethod
    def update_guest(self, guest: Guest) -> Guest:
        """Update an existing guest."""
        pass

    @abstractmethod
    def delete_guest(self, guest_id: int) -> None:
        """Delete a guest by ID."""
        pass
