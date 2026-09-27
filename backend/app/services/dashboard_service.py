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
            .where(Expense.ocr_confirmed.is_(True))
        ).one()
        today = date.today()
        month_total = self.db.scalar(
            select(func.coalesce(func.sum(Expense.total_amount), 0)).where(
                Expense.ocr_confirmed.is_(True),
                extract("year", Expense.invoice_date) == today.year,
                extract("month", Expense.invoice_date) == today.month,
            )
        )
        return {
            "total_expenses": f"{Decimal(total):.2f}",
            "expenses_this_month": f"{Decimal(month_total or 0):.2f}",
            "gst_paid": f"{Decimal(gst):.2f}",
            "expense_count": count,
        }
