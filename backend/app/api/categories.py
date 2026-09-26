from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.category import ExpenseCategory

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def list_categories(db: Session = Depends(get_db)):
    return [{"id": row.id, "name": row.name} for row in db.scalars(select(ExpenseCategory).order_by(ExpenseCategory.id))]

