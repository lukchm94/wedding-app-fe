from typing import Any, Dict, Optional

from fastapi import Request
from pydantic import BaseModel, Field

from ....modules.guests.domain.guest import GuestWithRsvpStatus


class FormInput(BaseModel):
    title: Optional[str] = Field(
        default="Potwierdzenie obecności",
        description="The title of the RSVP form or confirmation message.",
    )
    guest: GuestWithRsvpStatus = Field(
        ..., description="The guest object containing guest details."
    )
    plus_one: Optional[GuestWithRsvpStatus] = Field(
        default=None, description="The plus one guest object."
    )
    message: str = Field(
        default="obecność została potwierdzona: ",
        description="A message to be displayed on the RSVP form or confirmation page.",
    )
    success: bool = Field(
        default=True,
        description="Indicates whether the RSVP submission was successful.",
    )

    class Config:
        arbitrary_types_allowed = True

    @property
    def format_title(self) -> str:
        """
        Format the title for display.
        """
        return (
            f"{self.guest.first_name}"
            if self.plus_one is None
            else f"{self.guest.first_name} i {self.plus_one.first_name}"
        )

    @property
    def format_msg(self) -> str:
        prefix = "Wasza " if self.guest.has_guest and self.plus_one else "Twoja "
        return (
            f'{prefix}{self.message}{self.guest.rsvp_date.strftime("%d/%m/%Y")}'
            if self.guest.rsvp_date
            else "Nie potwierdzono obecności"
        )

    def as_dict(self, request: Request) -> Dict[str, Any]:
        """
        Convert the FormInput object to a dictionary.
        """
        return {
            "request": request,
            "title": self.format_title,
            "guest": self.guest,
            "plus_one": self.plus_one,
            "message": self.format_msg,
            "success": self.success,
        }
