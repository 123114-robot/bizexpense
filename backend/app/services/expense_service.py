from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.category import ExpenseCategory
from app.models.expense import Expense
from app.models.supplier import Supplier
from app.models.user import User
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseRead


class ExpenseService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ExpenseRepository(db)

    @staticmethod
    def serialize(expense: Expense) -> ExpenseRead:
        return ExpenseRead.model_validate({
            **{field: getattr(expense, field) for field in ExpenseRead.model_fields if hasattr(expense, field)},
            "supplier_name": expense.supplier.name,
            "category_name": expense.category.name,
        })

    def list(self, search: str | None = None) -> list[ExpenseRead]:
        return [self.serialize(item) for item in self.repo.list(search)]

    def get(self, expense_id: int) -> ExpenseRead:
        expense = self.repo.get(expense_id)
        if not expense:
            raise HTTPException(404, "Expense not found")
        return self.serialize(expense)

    def _references(self, payload: ExpenseCreate):
        user = self.db.scalar(select(User).limit(1))
        category = self.db.get(ExpenseCategory, payload.category_id)
        if not user or not category:
            raise HTTPException(422, "Invalid user or category")
        supplier = self.db.scalar(select(Supplier).where(Supplier.name == payload.supplier_name))
        if supplier is None:
            supplier = Supplier(name=payload.supplier_name, abn=payload.supplier_abn)
            self.db.add(supplier)
            self.db.flush()
        return user, supplier, category

    def create(self, payload: ExpenseCreate) -> ExpenseRead:
        user, supplier, category = self._references(payload)
        data = payload.model_dump(exclude={"supplier_name", "supplier_abn"})
        expense = Expense(**data, user_id=user.id, supplier_id=supplier.id, category_id=category.id)
        return self.serialize(self.repo.save(expense))

    def update(self, expense_id: int, payload: ExpenseCreate) -> ExpenseRead:
        expense = self.repo.get(expense_id)
        if not expense:
            raise HTTPException(404, "Expense not found")
        _, supplier, category = self._references(payload)
        for key, value in payload.model_dump(exclude={"supplier_name", "supplier_abn", "category_id"}).items():
            setattr(expense, key, value)
        expense.supplier_id = supplier.id
        expense.category_id = category.id
        return self.serialize(self.repo.save(expense))

    def delete(self, expense_id: int) -> None:
        expense = self.repo.get(expense_id)
        if not expense:
            raise HTTPException(404, "Expense not found")
        self.repo.delete(expense)

    # TODO: add non-blocking duplicate warning based on supplier + invoice_number + total_amount.

