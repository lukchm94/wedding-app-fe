from enum import Enum

from .utils.enums import ValidationEnum


class TokenTypes(str, ValidationEnum):
    bearer = "bearer"


class TokenConfigs(Enum):
    algorithm = "HS256"
    default_expiration = 30
