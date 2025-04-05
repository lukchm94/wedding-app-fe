from logging import Logger
from typing import Any

from ...domain.guest import Guest
from ...domain.service import GuestService


class CreateGuestUseCase:
    """
    Use case for creating a guest.
    """

    def __init__(self, guest_service: GuestService, logger: Logger) -> None:
        """
        Initialize the use case with a guest service and logger.
        """
        self.logger: Logger = logger
        self.guest_service: GuestService = guest_service

    def execute(self, guest_data: Any) -> Guest:
        """
        Execute the use case to create a guest.
        """
        # Validate the input data
        if not self._validate_guest_data(guest_data):
            raise ValueError("Invalid guest data")

        # Create the guest
        guest: Guest = self.guest_service.create_guest(guest_data)

        return guest

    def _validate_guest_data(self, guest_data) -> bool:
        """
        Validate the input data for creating a guest.
        """
        # Placeholder for validation logic
        return True
