from datetime import date
from decimal import Decimal

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.expense import Expense


class DashboardService:
    def __init__(self, db: Session):
        self.db = db

    def summary(self) -> dict:
        total, gst, count = self.db.execute(
            select(func.coalesce(func.sum(Expense.total_amount), 0), func.coalesce(func.sum(Expense.gst_amount), 0), func.count(Expense.id))
        ).one()
        today = date.today()
        month_total = self.db.scalar(
            select(func.coalesce(func.sum(Expense.total_amount), 0)).where(
                extract("year", Expense.invoice_date) == today.year,
                extract("month", Expense.invoice_date) == today.month,
            )
        )
        return {
            "total_expenses": Decimal(total).quantize(Decimal("0.01")),
            "expenses_this_month": Decimal(month_total or 0).quantize(Decimal("0.01")),
            "gst_paid": Decimal(gst).quantize(Decimal("0.01")),
            "expense_count": count,
        }

