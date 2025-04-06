from typing import Any

from ..domain.guest import Guest
from ..infra.repository.implementation import GuestRepoImpl


class GuestService:
    def __init__(self, guest_repository: GuestRepoImpl) -> None:
        self.guest_repository: GuestRepoImpl = guest_repository

    def get_guest(self, guest_id: int) -> Any:
        try:
            return self.guest_repository.get_guest_by_id(guest_id)
        except ValueError:
            return None

    def create_guest(self, guest_data: dict) -> Guest:
        return self.guest_repository.create_guest(guest_data)

    def update_guest(self, guest: Guest) -> Guest:
        return self.guest_repository.update_guest(guest)

    def find_guest_by_name(self, first_name: str, last_name: str) -> Guest:
        return self.guest_repository.find_guest_by_name(first_name, last_name)

    def delete_guest(self, guest_id: int) -> None:
        self.guest_repository.delete_guest(guest_id)
