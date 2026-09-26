from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import ExpenseCategory
from app.models.user import User

CATEGORIES = [
    "Office Supplies", "Fuel", "Travel", "Software", "Utilities", "Meals",
    "Equipment", "Professional Services", "Marketing", "Other",
]


def seed_reference_data(db: Session) -> None:
    if db.scalar(select(User).limit(1)) is None:
        db.add(User(name="Demo Admin", email="admin@bizexpense.local"))
    existing = set(db.scalars(select(ExpenseCategory.name)).all())
    db.add_all(ExpenseCategory(name=name) for name in CATEGORIES if name not in existing)
    db.commit()

