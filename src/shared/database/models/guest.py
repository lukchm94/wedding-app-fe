from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, DateTime, Enum, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ...utils.__validations import MenuChoices
from .base_model import BaseModel


class Guest(BaseModel):
    __tablename__ = "guests"

    first_name: Mapped[str] = mapped_column(String(50), nullable=False)
    last_name: Mapped[str] = mapped_column(String(50), nullable=False)
    email: Mapped[str] = mapped_column(
        String(255), unique=True, nullable=False, index=True
    )
    phone_number: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    rsvp_status: Mapped[str] = mapped_column(
        String(20), nullable=False, default="pending"
    )
    rsvp_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    has_guest: Mapped[Optional[bool]] = mapped_column(
        Boolean, nullable=True, default=False
    )
    guest_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    menu_choice: Mapped[Optional[MenuChoices]] = mapped_column(
        Enum(MenuChoices), nullable=True
    )
    dietary_restrictions: Mapped[Optional[str]] = mapped_column(
        String(255), nullable=True
    )
    hotel_accommodation: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    def __repr__(self):
        return f"<Guest {self.id} {self.first_name} {self.last_name}>"
