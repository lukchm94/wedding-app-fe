from typing import Annotated

from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from ...database.config import get_db
from ...database.models.user import User
from ...server.config import di_container
from ...utils.__validations import UserRoles
from ..models.logged_user import LoggedUser
from .user import get_current_user

logger = di_container.get_logger()


# Dependency to check if the user is an admin
async def get_current_admin_user(
    current_user: Annotated[LoggedUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> User | RedirectResponse:
    """
    Dependency to check if the current user is an admin.
    This will be used to protect admin routes.
    """
    logger.debug("Checking if current user is an admin")
    # If current_user is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(current_user, RedirectResponse):
        return current_user

    if current_user.role != UserRoles.ADMIN:
        # Redirect to login page instead of raising an exception
        return RedirectResponse(url="/login", status_code=303)

    # Get the full user from the database
    user = db.query(User).filter(User.username == current_user.username).first()
    if not user:
        logger.error("User not found in database")
        # Redirect to login page if user not found in database
        return RedirectResponse(url="/login", status_code=303)

    return user


# Dependency for admin routes
admin_dependency = Annotated[User, Depends(get_current_admin_user)]
