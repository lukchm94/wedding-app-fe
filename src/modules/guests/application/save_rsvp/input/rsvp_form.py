from typing import Optional

from pydantic import BaseModel, Field

from ....domain.guest import Guest


class RSVPFormData(BaseModel):
    first_name: str = Field(..., alias="firstName")
    last_name: str = Field(..., alias="lastName")
    menu: str = Field(..., alias="menu")
    dietary_requirements: Optional[str] = Field(None, alias="dietaryRequirements")
    phone: str = Field(..., alias="phone")
    email: str = Field(..., alias="email")
    needs_hotel: bool = Field(..., alias="needsHotel")
    has_guest: Optional[bool] = Field(None, alias="hasGuest")
    plus_one_first_name: Optional[str] = Field(None, alias="plusOneFirstName")
    plus_one_last_name: Optional[str] = Field(None, alias="plusOneLastName")
    plus_one_menu: Optional[str] = Field(None, alias="plusOneMenu")
    plus_one_dietary_requirements: Optional[str] = Field(
        None, alias="plusOneDietaryRequirements"
    )
    plus_one_phone: Optional[str] = Field(None, alias="plusOnePhone")
    plus_one_email: Optional[str] = Field(None, alias="plusOneEmail")

    class Config:
        populate_by_name = True


class ProcessedRSVPForm(BaseModel):
    guest: Guest
    plus_one: Optional[Guest]
