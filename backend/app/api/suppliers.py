from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.supplier import Supplier

router = APIRouter(prefix="/suppliers", tags=["suppliers"])


@router.get("")
def list_suppliers(db: Session = Depends(get_db)):
    return [{"id": row.id, "name": row.name, "abn": row.abn} for row in db.scalars(select(Supplier).order_by(Supplier.name))]

