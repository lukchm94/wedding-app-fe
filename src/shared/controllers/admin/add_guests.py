from typing import Optional

from pydantic import BaseModel, EmailStr

from src.modules.guests.domain.guest import Guest
from src.shared.utils.__validations import MenuChoices
from src.shared.utils.logger import Logger


class GuestDataCreate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    menu: str
    dietary_requirements: Optional[str] = None
    needs_hotel: bool


class GuestCreate(BaseModel):
    guest_data: GuestDataCreate
    has_guest: bool
    plus_one_data: Optional[GuestDataCreate] = None


class GuestController:
    def __init__(self, logger: Logger):
        self.logger = logger

    def create_guest(self, guest_data: GuestCreate) -> Guest:
        self.logger.debug(f"Creating guest: {guest_data.model_dump()}")
        guest = Guest(
            id=None,  # ID will be set by the database
            first_name=guest_data.guest_data.first_name,
            last_name=guest_data.guest_data.last_name,
            email=guest_data.guest_data.email,
            phone=guest_data.guest_data.phone,
            menu=MenuChoices(guest_data.guest_data.menu),
            dietary_requirements=guest_data.guest_data.dietary_requirements,
            needs_hotel=guest_data.guest_data.needs_hotel,
            has_guest=guest_data.has_guest,
            guest_id=None,
        )
        return guest

    def create_plus_one(self, guest_data: GuestCreate, guest_id: int) -> Guest:
        self.logger.debug(f"Creating plus one: {guest_data.model_dump()}")
        assert guest_data.plus_one_data, "Plus one data must be provided"
        plus_one = Guest(
            id=None,  # ID will be set by the database
            first_name=guest_data.plus_one_data.first_name,
            last_name=guest_data.plus_one_data.last_name,
            email=guest_data.plus_one_data.email,
            phone=guest_data.plus_one_data.phone,
            menu=MenuChoices(guest_data.plus_one_data.menu),
            dietary_requirements=guest_data.plus_one_data.dietary_requirements,
            needs_hotel=guest_data.plus_one_data.needs_hotel,
            has_guest=True,
            guest_id=guest_id,
        )
        return plus_one
