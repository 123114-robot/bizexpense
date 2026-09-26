import pytest
from pydantic import ValidationError

from app.schemas.expense import ExpenseCreate


def valid_payload(**changes):
    payload = {
        "supplier_name": "Acme",
        "category_id": 1,
        "invoice_date": "2026-09-01",
        "subtotal": "100.00",
        "gst_amount": "10.00",
        "total_amount": "110.00",
        "description": "Printer paper",
        "ocr_confirmed": True,
    }
    payload.update(changes)
    return payload


def test_valid_expense():
    assert ExpenseCreate(**valid_payload()).currency == "AUD"


@pytest.mark.parametrize("field", ["subtotal", "gst_amount", "total_amount"])
def test_negative_amount_rejected(field):
    with pytest.raises(ValidationError):
        ExpenseCreate(**valid_payload(**{field: "-1"}))


def test_gst_greater_than_total_rejected():
    with pytest.raises(ValidationError):
        ExpenseCreate(**valid_payload(gst_amount="120.00"))


def test_missing_required_values_rejected():
    payload = valid_payload()
    del payload["description"]
    with pytest.raises(ValidationError):
        ExpenseCreate(**payload)

