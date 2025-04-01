from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jose import ExpiredSignatureError, JWTError, jwt
from passlib.context import CryptContext

from ..__app_configs import TokenConfigs
from ..__exceptions import AuthenticationError, ExpiredTokenError, UserNotFoundError
from ..__settings import settings
from .models.logged_user import LoggedUser

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
token_dependency = Annotated[str, Depends(oauth2_bearer)]


# Dependency to get the Logged User
async def get_current_user(token: token_dependency) -> LoggedUser:
    try:
        payload = jwt.decode(
            token=token,
            key=settings.SECRET_KEY,
            algorithms=[TokenConfigs.algorithm.value],
        )
        username: str = payload.get("sub")
        user_role: str = payload.get("role")
        permissions: str = payload.get("permissions")
        if username is None:
            raise UserNotFoundError(username=username)
        return LoggedUser(username=username, role=user_role, permissions=permissions)

    except ExpiredSignatureError:
        raise ExpiredTokenError()

    except JWTError:
        raise AuthenticationError(username)


user_dependency = Annotated[LoggedUser, Depends(get_current_user)]
