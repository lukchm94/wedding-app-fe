from logging import Logger

from sqlalchemy.orm import Session
from typing_extensions import override

from src.shared.database.models.user import User as UserModelDB

from ...domain.user_model import UserModel
from ...domain.user_repository import UserRepository


class UserRepoImpl(UserRepository):
    def __init__(self, db: Session, logger: Logger) -> None:
        self.db: Session = db
        self.logger: Logger = logger
        self.logger.debug("UserRepoImpl initialized")
        self.logger.debug(f"Database session: {self.db}")
        self.logger.debug(f"Type of DB: {type(self.db)}")

    @override
    def get_user_by_email(self, email: str) -> UserModel:
        """Retrieve a user by email."""
        self.logger.debug(f"Retrieving user by email: {email}")
        user: UserModelDB = (
            self.db.query(UserModelDB).filter(UserModelDB.email == email).first()
        )
        self.db.query(UserModelDB).filter(UserModelDB.email == email).first()
        if not user:
            raise ValueError(f"User with email {email} not found.")
        user = UserModel.from_orm(user)
        return super().get_user_by_email(email)

    @override
    def create_user(self, user: UserModel) -> UserModel:
        user_model: UserModelDB = UserModelDB(**user.model_dump())
        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)
        self.logger.info(f"User created: {user_model}")
        return user

    @override
    def get_user_by_id(self, user_id: int) -> UserModel:
        user: UserModelDB = (
            self.db.query(UserModelDB).filter(UserModelDB.id == user_id).first()
        )
        if not user:
            raise ValueError(f"User with ID {user_id} not found.")
        return UserModel.from_orm(user)

    @override
    def update_user(self, user: UserModel) -> UserModel:
        existing_user = (
            self.db.query(UserModelDB).filter(UserModelDB.id == user.user_id).first()
        )
        if not existing_user:
            raise ValueError(f"User with ID {user.user_id} not found.")
        for key, value in user.model_dump().items():
            setattr(existing_user, key, value)
        self.db.commit()
        self.db.refresh(existing_user)
        return existing_user

    @override
    def delete_user(self, user_id: int) -> None:
        user = self.get_user_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        self.logger.info(f"User with ID {user_id} deleted.")
        return None
