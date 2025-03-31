from logging import Logger
from typing import TYPE_CHECKING, Optional

from sqlalchemy.orm import Session
from typing_extensions import override

from src.shared.database.models.guest import Guest as GuestModel

from ...domain.guest import Guest
from ...domain.repository import GuestRepository


class GuestRepoImpl(GuestRepository):
    def __init__(self, db: Session, logger: Logger) -> None:
        self.db: Session = db
        self.logger: Logger = logger

    @override
    def create_guest(self, guest: str) -> Guest:
        """Create a new guest."""
        guest_model: GuestModel = GuestModel(guest.model_dump())
        self.db.add(guest_model)
        self.db.commit()
        self.db.refresh(guest_model)
        self.logger.info(f"Guest created: {guest_model}")
        return guest

    @override
    def get_guest_by_id(self, guest_id: int) -> Optional[GuestModel]:
        """Retrieve a guest by ID."""
        guest: GuestModel = (
            self.db.query(GuestModel).filter(GuestModel.id == guest_id).first()
        )
        if not guest:
            raise ValueError(f"Guest with ID {guest_id} not found.")
        return Guest.from_orm(guest)

    @override
    def update_guest(self, guest: Guest) -> GuestModel:
        """Update an existing guest."""
        existing_guest = (
            self.db.query(GuestModel).filter(GuestModel.id == guest.guest_id).first()
        )
        if not existing_guest:
            raise ValueError(f"Guest with ID {guest.guest_id} not found.")
        for key, value in guest.model_dump().items():
            setattr(existing_guest, key, value)
        self.db.commit()
        self.db.refresh(existing_guest)
        return existing_guest

    @override
    def delete_guest(self, guest_id: int) -> None:
        """Delete a guest by ID."""
        guest = self.get_guest_by_id(guest_id)
        if guest:
            self.db.delete(guest)
            self.db.commit()
