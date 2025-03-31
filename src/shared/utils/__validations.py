from enum import Enum


class RsvpStatus(str, Enum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"


class UserRoles(str, Enum):
    ADMIN = "admin"
    GUEST = "guest"


class MenuChoices(str, Enum):
    MEAT = "Menu mięsne"
    VEGETARIAN = "Menu wegetariańskie"
    VEGAN = "Menu wegańskie"
