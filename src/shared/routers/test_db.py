from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.shared.database.config import engine, get_db
from src.shared.database.models import Base

router = APIRouter(prefix="/test", tags=["test"])


@router.get("/db")
async def test_db(db: Session = Depends(get_db)):
    try:
        # Try to create tables
        Base.metadata.create_all(bind=engine)
        return {
            "message": "Database connection successful!",
            "tables": Base.metadata.tables.keys(),
        }
    except Exception as e:
        return {"error": str(e)}
