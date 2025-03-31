from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.shared.__settings import settings

SQLALCHEMY_DATABASE_URL = settings.DATABASE_URL

print(f"SQLALCHEMY_DATABASE_URL: {SQLALCHEMY_DATABASE_URL}")

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

print(f"engine: {engine}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

print(f"SessionLocal: {SessionLocal}")
Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
