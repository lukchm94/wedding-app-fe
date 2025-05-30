from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional

from ....shared.utils.__validations import RsvpStatus
from .guest import Guest, GuestWithRsvpStatus


class GuestRepository(ABC):
    @abstractmethod
    def get_guest_by_id(self, guest_id: int) -> Optional[GuestWithRsvpStatus]:
        """Retrieve a guest by ID."""
        pass

    @abstractmethod
    def find_guest_by_name(
        self, first_name: str, last_name: str
    ) -> Optional[GuestWithRsvpStatus]:
        """Find a guest by first and last name."""
        pass

    @abstractmethod
    def create_guest(self, guest: Guest) -> Guest:
        """Create a new guest."""
        pass

    @abstractmethod
    def update_guest(
        self, guest: Guest, status: RsvpStatus, submitted_at: datetime
    ) -> Guest:
        """Update an existing guest."""
        pass

    @abstractmethod
    def delete_guest(self, guest_id: int) -> None:
        """Delete a guest by ID."""
        pass

    @abstractmethod
    def find_in_session(self, first_name: str) -> list[Guest]:
        """Find guests in the session by first name."""
        pass
