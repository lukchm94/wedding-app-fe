from datetime import datetime
from typing import Optional

from src.modules.guests.domain.guest import Guest
from src.modules.guests.domain.service import GuestService
from src.shared.utils.__validations import RsvpStatus
from src.shared.utils.logger import Logger


class UpdateGuestUseCase:
    def __init__(self, guest_service: GuestService, logger: Logger):
        self.guest_service = guest_service
        self.logger = logger

    def execute(
        self,
        guest: Guest,
        status: RsvpStatus = RsvpStatus.PENDING,
        submitted_at: Optional[datetime] = None,
    ) -> Guest:
        self.logger.debug(f"Updating\n\nInside UpdateGuestUseCase\n\n")
        return self.guest_service.update_guest(guest, status, submitted_at)
