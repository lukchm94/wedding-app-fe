from typing import Optional, Union, overload

from src.modules.guests.domain.guest import Guest
from src.modules.guests.domain.repository import GuestRepository
from src.modules.guests.domain.service import GuestService


class FindGuestUseCase:
    def __init__(self, guest_service: GuestService):
        self.guest_service: GuestService = guest_service

    def execute(
        self,
        guest_id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Union[Guest, None]:
        """
        Find guests either by ID or by name.

        Args:
            guest_id: Optional ID to find a specific guest
            first_name: Optional first name to search for
            last_name: Optional last name to search for

        Returns:
            A single Guest if searching by ID, or a list of Guests if searching by name
        """
        print(
            f"Searching for guests with guest_id: {guest_id}, first_name: {first_name}, last_name: {last_name}"
        )
        print(guest_id is not None and isinstance(guest_id, int))
        # If guest_id is provided and it's an integer, search by ID
        if guest_id is not None and isinstance(guest_id, int):
            return self.guest_service.get_guest(guest_id)

        # Otherwise, search by name
        print(first_name is not None and last_name is not None)
        guest: Guest = self.guest_service.find_guest_by_name(first_name, last_name)
        print(f"\n\nGuest in use case: {guest}\n\n")
        return guest
