from datetime import datetime
from typing import Optional, Union

from ....shared.utils.__validations import RsvpStatus
from ..domain.guest import Guest, GuestWithRsvpStatus
from ..infra.repository.implementation import GuestRepoImpl


class GuestService:
    def __init__(self, guest_repository: GuestRepoImpl) -> None:
        self.guest_repository: GuestRepoImpl = guest_repository

    def get_guest(self, guest_id: int) -> Union[GuestWithRsvpStatus, None]:
        try:
            return self.guest_repository.get_guest_by_id(guest_id)
        except ValueError:
            return None

    def create_guest(self, guest_data: Guest) -> Guest:
        return self.guest_repository.create_guest(guest_data)

    def update_guest(
        self, guest: Guest, status: RsvpStatus, submitted_at: Optional[datetime] = None
    ) -> Guest:
        return self.guest_repository.update_guest(guest, status, submitted_at)

    def find_guest_by_name(
        self, first_name: str, last_name: str
    ) -> GuestWithRsvpStatus | None:
        return self.guest_repository.find_guest_by_name(first_name, last_name)

    def delete_guest(self, guest_id: int) -> None:
        self.guest_repository.delete_guest(guest_id)

    def find_in_session(self, first_name: str) -> list[Guest]:
        return self.guest_repository.find_in_session(first_name)
