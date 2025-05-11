from logging import Logger
from typing import Union

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

    def execute(self, guest: Guest) -> Guest:
        """
        Execute the use case to create a guest.
        """
        # Validate the input data
        if not self._validate_guest_data(guest):
            raise ValueError("Invalid guest data")

        # Log the guest data being created
        self.logger.info(f"Creating guest: {guest.model_dump()}")

        # Create the guest
        created_guest: Guest = self.guest_service.create_guest(guest)

        return created_guest

    def _validate_guest_data(self, guest: Union[Guest, None]) -> bool:
        """
        Validate the input data for creating a guest.
        """
        # Check if the guest data is valid
        if not guest:
            self.logger.error("Guest data is missing")
            return False

        # Check if guest_id is provided when has_guest is True
        if guest.has_guest and not guest.guest_id:
            # This is okay, as we'll set the guest_id after creating the plus-one
            self.logger.info(
                "Guest ID is not set yet, will be set after creating the plus-one"
            )
            return True

        return True
