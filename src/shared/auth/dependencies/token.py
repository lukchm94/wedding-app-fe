from typing import Annotated

from fastapi import Depends, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordBearer

from ...server.config import di_container

# Update OAuth2PasswordBearer to use cookies
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token", auto_error=False)
logger = di_container.get_logger()


# Custom dependency to get the token from cookies
async def get_token_from_cookie(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        logger.error("No token found in cookies")
        # Redirect to login page instead of raising an exception
        return RedirectResponse(url="/login", status_code=303)
    # Remove "Bearer " prefix if present
    if token.startswith("Bearer "):
        logger.debug("Token found in cookies")
        token = token[7:]
    return token


token_dependency = Annotated[str, Depends(get_token_from_cookie)]
