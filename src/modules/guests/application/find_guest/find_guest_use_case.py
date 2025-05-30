from typing import Optional, Union

from .....shared.utils.logger import logger
from ...domain.guest import Guest, GuestWithRsvpStatus
from ...domain.service import GuestService


class FindGuestUseCase:
    def __init__(self, guest_service: GuestService):
        self.guest_service: GuestService = guest_service

    def execute(
        self,
        guest_id: Optional[int] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
    ) -> Union[GuestWithRsvpStatus, None]:
        """
        Find guests either by ID or by name.

        Args:
            guest_id: Optional ID to find a specific guest
            first_name: Optional first name to search for
            last_name: Optional last name to search for

        Returns:
            A single Guest if searching by ID, or a list of Guests if searching by name
        """
        logger.info(
            f"Searching for guests with guest_id: {guest_id}, first_name: {first_name}, last_name: {last_name}"
        )
        # If guest_id is provided and it's an integer, search by ID
        if guest_id is not None and isinstance(guest_id, int):  # type: ignore
            return self.guest_service.get_guest(guest_id)

        assert first_name is not None
        assert isinstance(first_name, str), "First name must be a string"
        assert last_name is None or isinstance(last_name, str)
        assert isinstance(last_name, str), "Last name must be a string"

        guest: GuestWithRsvpStatus | None = self.guest_service.find_guest_by_name(
            first_name, last_name
        )
        return guest

    def find_in_session(self, first_name: str) -> list[Guest]:
        """
        The function `find_in_session` takes a first name as input and returns a list of `Guest` objects
        found in the session.

        :param first_name: The `first_name` parameter in the `find_in_session` method is a string that
        represents the first name of a guest. This method is used to search for guests in a session
        based on their first name
        :type first_name: str
        :return: A list of Guest objects that match the provided first name in the session.
        """
        return self.guest_service.find_in_session(first_name)
