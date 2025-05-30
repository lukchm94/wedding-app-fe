from __future__ import annotations

import re
from datetime import datetime
from typing import Any, Dict, Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from ....shared.database.models.guest import Guest as GuestModel
from ....shared.utils.__validations import MenuChoices, RsvpStatus
from ....shared.utils.logger import logger


class Guest(BaseModel):
    """
    Represents a guest in the system.
    """

    id: Optional[int] = Field(None, description="ID of the guest")
    first_name: str = Field(..., description="First name of the guest")
    last_name: str = Field(..., description="Last name of the guest")
    has_guest: bool = Field(
        ..., description="Indicates if the guest is bringing a plus one"
    )
    guest_id: Optional[int] = Field(None, description="ID of the accompanying guest")
    menu: MenuChoices = Field(..., description="Menu choice for the guest")
    dietary_requirements: Optional[str] = Field(
        None, description="Dietary restrictions or requirements"
    )
    needs_hotel: bool = Field(
        ..., description="Indicates if the guest needs hotel accommodation"
    )
    phone: str = Field(..., description="Phone number of the guest")
    email: EmailStr = Field(..., description="Email address of the guest")

    @model_validator(mode="after")
    def validate_guest(self):
        """
        Custom validation logic for the Guest model.
        """
        # Validate phone number format
        phone_pattern = r"^\d{3}-\d{3}-\d{3}$"
        if not re.match(phone_pattern, self.phone):
            raise ValueError("Phone number must be in the format xxx-xxx-xxx.")

        email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_pattern, self.email):
            raise ValueError("Email must be in the format example@example.com.")

        # Validate guest ID if has_guest is True
        if self.has_guest and not self.guest_id:
            logger.warning(
                f"Guest ID must be provided if 'has_guest' is True. Forcing guest ID to 0. for guest: {self.first_name} {self.last_name} {self.email}"
            )
            # assert self.id is not None, "Guest ID must be set if has_guest is True"
            self.guest_id = 0

        self.first_name = self.first_name.lower().capitalize()
        self.last_name = self.last_name.lower().capitalize()

        return self

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Guest:
        """
        Create a Guest instance from a dictionary.
        """
        return cls(**data)

    @staticmethod
    def from_orm(obj: GuestModel) -> "Guest":  # type: ignore
        """
        Create a Guest instance from an ORM model.
        """
        assert isinstance(obj, GuestModel)
        assert obj.phone_number
        return Guest(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            has_guest=obj.has_guest if obj.has_guest is not None else False,
            guest_id=obj.guest_id,
            menu=MenuChoices(obj.menu_choice),
            dietary_requirements=obj.dietary_restrictions,
            needs_hotel=obj.hotel_accommodation,
            phone=obj.phone_number,
            email=obj.email,
        )


class GuestWithRsvpStatus(Guest):
    """
    Represents a guest in the system, specifically for ORM operations.
    """

    rsvp_status: RsvpStatus = Field(..., description="RSVP status of the guest")
    rsvp_date: Optional[datetime] = Field(
        default=None, description="Date and time when the RSVP was submitted"
    )

    @staticmethod
    def from_orm(obj: GuestModel) -> "GuestWithRsvpStatus":  # type: ignore
        """
        Create a GuestWithRsvpStatus instance from an ORM model.
        """
        assert isinstance(obj, GuestModel)
        assert obj.phone_number

        # Create base guest first
        base_guest = Guest.from_orm(obj)

        # Add RSVP specific fields
        return GuestWithRsvpStatus(
            **base_guest.model_dump(),  # Use base guest fields
            rsvp_status=RsvpStatus(obj.rsvp_status),
            rsvp_date=obj.rsvp_date,
        )
