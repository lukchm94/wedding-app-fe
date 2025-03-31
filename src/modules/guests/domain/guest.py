from __future__ import annotations

import re
from typing import Optional

from pydantic import BaseModel, EmailStr, Field, model_validator

from .....src.shared.database.models.guest import Guest as GuestModel
from .....src.shared.utils.__validations import MenuChoices


class Guest(BaseModel):
    first_name: str = Field(..., description="First name of the guest")
    last_name: str = Field(..., description="Last name of the guest")
    has_guest: bool = Field(
        ..., description="Indicates if the guest is bringing a plus one"
    )
    guest_id: Optional[int] = Field(None, description="ID of the accompanying guest")
    menu: MenuChoices = Field(..., description="Menu choice for the guest")
    dietary_requirements: str = Field(
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

        # Validate guest ID if has_guest is True
        if self.has_guest and not self.guest_id:
            raise ValueError("Guest ID must be provided if 'has_guest' is True.")

        # Validate menu choice if has_guest is True
        if self.has_guest and self.menu == MenuChoices.VEGAN:
            raise ValueError(
                "Guests cannot select a vegan menu if they are bringing a plus one."
            )

        return self

    def from_dict(cls, data: dict) -> Guest:
        """
        Create a Guest instance from a dictionary.
        """
        return cls(**data)

    def from_orm(cls, data: GuestModel) -> Guest:
        """
        Create a Guest instance from an ORM model.
        """
        return Guest(
            first_name=data.first_name,
            last_name=data.last_name,
            has_guest=data.has_guest,
            guest_id=data.guest_id,
            menu=MenuChoices(data.menu_choice),
            dietary_requirements=data.dietary_restrictions,
            needs_hotel=data.hotel_accommodation,
            phone=data.phone_number,
            email=data.email,
        )
