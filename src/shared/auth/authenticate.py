from passlib.context import CryptContext

from .dependencies import (
    admin_dependency,
    get_current_admin_user,
    get_current_user,
    get_token_from_cookie,
    token_dependency,
    user_dependency,
)

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Re-export dependencies for backward compatibility
__all__ = [
    "token_dependency",
    "get_token_from_cookie",
    "user_dependency",
    "get_current_user",
    "admin_dependency",
    "get_current_admin_user",
]
