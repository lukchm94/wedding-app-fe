from logging import Logger
from typing import Optional, Union

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
    def create_guest(self, guest: Guest) -> Guest:
        """Create a new guest."""
        existing_guest: Union[GuestModel, None] = (
            self.db.query(GuestModel).filter(GuestModel.email == guest.email).first()
        )
        if existing_guest:
            return self.update_guest(guest)

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
        return guest

    @override
    def get_guest_by_id(self, guest_id: int) -> Optional[GuestModel]:
        """Retrieve a guest by ID."""
        guest: Union[GuestModel, None] = (
            self.db.query(GuestModel).filter(GuestModel.id == guest_id).first()
        )
        if not guest:
            raise ValueError(f"Guest with ID {guest_id} not found.")
        return Guest.from_orm(guest)

    @override
    def update_guest(self, guest: Guest) -> GuestModel:
        """Update an existing guest."""
        existing_guest = (
            self.db.query(GuestModel).filter(GuestModel.email == guest.email).first()
        )
        if not existing_guest:
            raise ValueError(f"Guest with email {guest.email} not found.")

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

        # Update the ORM model with the mapped dictionary
        for key, value in orm_guest_dict.items():
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
