from enum import Enum

from .utils.enums import ValidationEnum


class TokenTypes(str, ValidationEnum):
    bearer = "bearer"


class TokenConfigs(Enum):
    algorithm: str = "HS256"
    default_expiration: int = 30
