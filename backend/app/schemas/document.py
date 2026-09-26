from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class DocumentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    original_filename: str
    mime_type: str
    uploaded_at: datetime


class OCRResult(BaseModel):
    supplier_name: str
    abn: str | None = None
    invoice_number: str | None = None
    invoice_date: date
    due_date: date | None = None
    subtotal: Decimal
    gst: Decimal
    total: Decimal
    currency: str = "AUD"
    confidence: float
    confirmed: bool = False

