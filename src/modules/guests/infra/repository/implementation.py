from datetime import datetime
from logging import Logger
from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session
from typing_extensions import override

from .....shared.database.models.guest import Guest as GuestModel
from .....shared.utils.__validations import RsvpStatus
from ...domain.guest import Guest, GuestWithRsvpStatus
from ...domain.repository import GuestRepository


class GuestRepoImpl(GuestRepository):
    def __init__(self, db: Session, logger: Logger) -> None:
        self.db: Session = db
        self.logger: Logger = logger
        self.logger.info(f"[{self.__class__.__name__}] initialized.")

    @override
    def create_guest(self, guest: Guest) -> Guest:
        """Create a new guest."""
        # Check for existing guest with same first and last name
        existing_guest_name: Union[GuestModel, None] = (
            self.db.query(GuestModel)
            .filter(
                GuestModel.first_name == guest.first_name,
                GuestModel.last_name == guest.last_name,
            )
            .first()
        )
        if existing_guest_name:
            self.logger.info(
                f"Guest with name {guest.first_name} {guest.last_name} already exists: {existing_guest_name}"
            )
            raise ValueError(
                f"Guest with name {guest.first_name} {guest.last_name} already exists"
            )

        # Convert the Guest domain model to a dictionary
        guest_dict = guest.model_dump()

        # Map the domain model fields to the ORM model fields
        orm_guest_dict = {
            "first_name": guest_dict["first_name"],
            "last_name": guest_dict["last_name"],
            "email": guest_dict["email"],
            "phone_number": guest_dict["phone"],
            "menu_choice": guest_dict["menu"],
            "dietary_restrictions": guest_dict["dietary_requirements"],
            "hotel_accommodation": guest_dict["needs_hotel"],
            "has_guest": guest_dict["has_guest"],
            "guest_id": guest_dict["guest_id"],
        }

        # Create the ORM model with the mapped dictionary
        guest_model: GuestModel = GuestModel(**orm_guest_dict)

        self.db.add(guest_model)
        self.db.commit()
        self.db.refresh(guest_model)
        self.logger.info(f"Guest created: {guest_model}")
        # guest = Guest.from_orm(guest_model)
        self.logger.info(f"Guest Model ID: {guest_model.id}")

        return Guest.from_orm(guest_model)

    @override
    def get_guest_by_id(self, guest_id: int) -> Optional[GuestWithRsvpStatus]:
        """Retrieve a guest by ID."""
        guest: Union[GuestModel, None] = (
            self.db.query(GuestModel).filter(GuestModel.id == guest_id).first()
        )
        self.logger.debug(f"[{self.__class__}] Retrieved guest: {guest}")
        if not guest:
            return None
        return GuestWithRsvpStatus.from_orm(guest)

    @override
    def update_guest(
        self, guest: Guest, status: RsvpStatus, submitted_at: Optional[datetime] = None
    ) -> Guest:
        """Update an existing guest."""
        existing_guest = (
            self.db.query(GuestModel).filter(GuestModel.id == guest.id).first()
        )
        self.logger.debug(f"Existing guest: {existing_guest}")
        if not existing_guest:
            raise ValueError(f"Guest with ID {guest.id} not found.")

        # Convert the Guest domain model to a dictionary
        guest_dict: Dict[str, Any] = guest.model_dump()

        # Map the domain model fields to the ORM model fields
        orm_guest_dict: Dict[str, Any] = {
            "first_name": guest_dict["first_name"],
            "last_name": guest_dict["last_name"],
            "email": guest_dict["email"],
            "phone_number": guest_dict["phone"],
            "menu_choice": guest_dict["menu"],
            "dietary_restrictions": guest_dict["dietary_requirements"],
            "hotel_accommodation": guest_dict["needs_hotel"],
            "has_guest": guest_dict["has_guest"],
            "guest_id": guest_dict["guest_id"],
            "rsvp_status": status.value,
            "rsvp_date": submitted_at,
        }

        self.logger.debug(f"ORM guest dict: {orm_guest_dict}")

        # Update the ORM model with the mapped dictionary
        for key, value in orm_guest_dict.items():
            setattr(existing_guest, key, value)

        self.db.commit()
        self.db.refresh(existing_guest)

        return guest

    @override
    def delete_guest(self, guest_id: int) -> None:
        """Delete a guest by ID."""
        guest = self.get_guest_by_id(guest_id)
        if guest:
            self.db.delete(guest)
            self.db.commit()

    @override
    def find_guest_by_name(
        self, first_name: str, last_name: str
    ) -> Optional[GuestWithRsvpStatus]:
        """Find a guest by first and last name."""
        guest_model: Union[GuestModel, None] = (
            self.db.query(GuestModel)
            .filter(
                GuestModel.first_name == first_name, GuestModel.last_name == last_name
            )
            .first()
        )
        self.logger.debug(f"\n\nGuest ORM Model: {guest_model}\n\n")

        # Check if guest_model is None before trying to convert it
        if guest_model is None:
            return None

        guest: GuestWithRsvpStatus = GuestWithRsvpStatus.from_orm(guest_model)
        self.logger.debug(f"\n\nGuest: {guest}\n\n")
        return guest

    @override
    def find_in_session(self, first_name: str) -> list[Guest | GuestWithRsvpStatus]:
        """Find a guest by first name."""
        guests: list[GuestModel] = (
            self.db.query(GuestModel)
            .filter(GuestModel.first_name.ilike(f"%{first_name}%"))
            .all()
        )
        return [Guest.from_orm(guest) for guest in guests]
