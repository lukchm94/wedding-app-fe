from typing import Optional

from pydantic import BaseModel

from ....domain.guest import Guest


class SavedGuests(BaseModel):
    guest: Guest
    plus_one: Optional[Guest]

    @property
    def formatted_names(self) -> str:
        if not self.plus_one:
            return self.guest.first_name
        return f"{self.guest.first_name} i {self.plus_one.first_name}"

    @property
    def message(self) -> str:
        return "Dzięlujemy za potwierdzenie obecności"
