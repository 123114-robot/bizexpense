import csv
from datetime import date
from io import StringIO

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.expense import ExpenseCreate, ExpenseRead, ExpenseUpdate
from app.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["expenses"])


def _csv_safe(value: object) -> str:
    text = "" if value is None else str(value)
    return f"'{text}" if text.startswith(("=", "+", "-", "@")) else text


def _filtered_expenses(
    db: Session,
    search: str | None,
    category_id: int | None,
    date_from: date | None,
    date_to: date | None,
    ocr_confirmed: bool | None,
) -> list[ExpenseRead]:
    return ExpenseService(db).list(
        search, category_id, date_from, date_to, ocr_confirmed
    )


@router.get("", response_model=list[ExpenseRead])
def list_expenses(
    search: str | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    ocr_confirmed: bool | None = None,
    db: Session = Depends(get_db),
):
    return _filtered_expenses(
        db, search, category_id, date_from, date_to, ocr_confirmed
    )


@router.get("/export.csv")
def export_expenses(
    search: str | None = None,
    category_id: int | None = None,
    date_from: date | None = None,
    date_to: date | None = None,
    ocr_confirmed: bool | None = None,
    db: Session = Depends(get_db),
):
    expenses = _filtered_expenses(
        db, search, category_id, date_from, date_to, ocr_confirmed
    )
    output = StringIO()
    writer = csv.writer(output, lineterminator="\n")
    writer.writerow(
        [
            "Date",
            "Supplier",
            "Invoice number",
            "Category",
            "Description",
            "Subtotal",
            "GST",
            "Total",
            "Currency",
            "Status",
        ]
    )
    for expense in expenses:
        writer.writerow(
            map(
                _csv_safe,
                [
                    expense.invoice_date,
                    expense.supplier_name,
                    expense.invoice_number or "",
                    expense.category_name,
                    expense.description,
                    expense.subtotal,
                    expense.gst_amount,
                    expense.total_amount,
                    expense.currency,
                    "Confirmed" if expense.ocr_confirmed else "Draft",
                ],
            )
        )
    return Response(
        content="\ufeff" + output.getvalue(),
        media_type="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": "attachment; filename=bizexpense-expenses.csv"
        },
    )


@router.post("", response_model=ExpenseRead, status_code=status.HTTP_201_CREATED)
def create_expense(payload: ExpenseCreate, db: Session = Depends(get_db)):
    return ExpenseService(db).create(payload)


@router.get("/{expense_id}", response_model=ExpenseRead)
def get_expense(expense_id: int, db: Session = Depends(get_db)):
    return ExpenseService(db).get(expense_id)


@router.put("/{expense_id}", response_model=ExpenseRead)
def update_expense(expense_id: int, payload: ExpenseUpdate, db: Session = Depends(get_db)):
    return ExpenseService(db).update(expense_id, payload)


@router.delete("/{expense_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    ExpenseService(db).delete(expense_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
