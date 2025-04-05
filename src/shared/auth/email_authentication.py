from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..database.models.user import User
from ..utils.__validations import UserRoles
from ..utils.logger import logger


def authenticate_admin(email: str, password: str, db: Session) -> User:
    """
    Authenticate the user by email and check if they have admin access.
    """
    user = db.query(User).filter(User.email == email).first()
    if not user or not user.role == UserRoles.ADMIN:
        logger.error(f"Access denied for user: {email}")
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")
    if user.hashed_password != password:
        logger.error(f"Invalid password for user: {email}")
        raise HTTPException(status_code=401, detail="Invalid credentials.")
    return user
