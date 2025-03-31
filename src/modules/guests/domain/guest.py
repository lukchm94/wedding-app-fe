from typing import Optional

from pydantic import BaseModel


class Guest(BaseModel):
    first_name: str
    last_name: str
    has_guest: bool
    guest_name: Optional[str] = None
    menu: str
    dietary_requirements: Optional[str] = None
    needs_hotel: bool
    phone: str
    email: str
