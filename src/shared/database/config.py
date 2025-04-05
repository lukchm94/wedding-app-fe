from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.shared.__settings import settings
from src.shared.utils.logger import logger

SQLALCHEMY_DATABASE_URL: str = settings.DATABASE_URL

logger.info(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Error in session_scope: {e}")
        raise
    finally:
        db.close()
        logger.debug("Session closed")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
