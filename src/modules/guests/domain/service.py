from typing import Any

from ..domain.guest import Guest
from .repository import GuestRepository


class GuestService:
    def __init__(self, guest_repository: GuestRepository) -> None:
        self.guest_repository: GuestRepository = guest_repository

    def get_guest(self, guest_id: int) -> Any:
        return self.guest_repository.get_guest_by_id(guest_id)

    def create_guest(self, guest_data: dict) -> Guest:
        return self.guest_repository.create_guest(guest_data)

    def update_guest(self, guest_id: int, guest_data: dict) -> Any:
        return self.guest_repository.update_guest(guest_id, guest_data)

    def delete_guest(self, guest_id: int) -> None:
        self.guest_repository.delete_guest(guest_id)
