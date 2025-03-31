from sqlalchemy import Boolean, Column, DateTime, Enum, Integer, String

from src.shared.database.models.base import BaseModel

from ...utils.__validations import MenuChoices


class Guest(BaseModel):
    __tablename__ = "guests"

    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    phone_number = Column(String(20), nullable=True)
    rsvp_status = Column(String(20), nullable=False, default="pending")
    rsvp_date = Column(DateTime, nullable=True)
    has_guest = Column(Boolean(20), nullable=True, default=False)
    guest_id = Column(Integer, nullable=True)
    menu_choice = Column(Enum(MenuChoices), nullable=True)
    dietary_restrictions = Column(String(255), nullable=True)
    hotel_accommodation = Column(Boolean(20), nullable=False, default=False)

    def __repr__(self):
        return f"<Guest {self.id} {self.first_name} {self.last_name}>"
