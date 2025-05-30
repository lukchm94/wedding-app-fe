from typing import Annotated, Union

from fastapi import Depends
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, JWTError, jwt

from ...__app_configs import TokenConfigs
from ...__exceptions import UserNotFoundError
from ...__settings import settings
from ...server.config import di_container
from ...utils.__validations import UserRoles
from ..models.logged_user import LoggedUser
from .token import get_token_from_cookie

logger = di_container.get_logger()


# Dependency to get the Logged User
async def get_current_user(
    token: Annotated[str, Depends(get_token_from_cookie)],
) -> LoggedUser | RedirectResponse:
    # If token is a RedirectResponse, return it (this means user is not authenticated)
    if isinstance(token, RedirectResponse):
        return token

    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[TokenConfigs.algorithm.value],
        )
        username: Union[str, None] = payload.get("sub")
        user_role: str = str(payload.get("role"))
        permissions: str = str(payload.get("permissions"))
        if username is None:
            raise UserNotFoundError(username=username)
        return LoggedUser(
            username=username,
            role=UserRoles[user_role.upper()],  # Convert string to enum
            permissions=permissions,
        )

    except ExpiredSignatureError:
        # Redirect to login page on expired token
        return RedirectResponse(url="/login", status_code=303)

    except JWTError:
        # Redirect to login page on invalid token
        return RedirectResponse(url="/login", status_code=303)


user_dependency = Annotated[LoggedUser, Depends(get_current_user)]
