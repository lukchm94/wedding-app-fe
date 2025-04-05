from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ..database.config import get_db
from ..database.models.user import User as UserModel
from ..utils.logger import logger

router = APIRouter(prefix="/users", tags=["users"])
db_session = Annotated[Session, Depends(get_db)]

TEST_USER = UserModel(
    username="admin",
    email="admin@admin.com",
    role="admin",
    hashed_password="hashed_password",
)


@router.post("/")
async def create_user(db: db_session, request: Request):
    logger.info("Creating user")

    db.add(TEST_USER)
    db.commit()
    db.refresh(TEST_USER)
    logger.info(f"User created: {TEST_USER}")
    # Placeholder for user creation logic
    return {"message": "User created successfully", "data": TEST_USER}


@router.get("/")
async def get_user(db: db_session):
    logger.info("Getting user")
    users = db.query(UserModel).all()
    logger.info(f"Users retrieved: {users}")
    # Placeholder for user retrieval logic
    return {"message": "Users retrieved successfully", "data": users}
