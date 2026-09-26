from abc import ABC, abstractmethod
from datetime import date, timedelta
from decimal import Decimal

from app.schemas.document import OCRResult


class OCRProvider(ABC):
    @abstractmethod
    def extract(self, file_path: str) -> OCRResult: ...


class MockOCRProvider(OCRProvider):
    def extract(self, file_path: str) -> OCRResult:
        today = date.today()
        return OCRResult(
            supplier_name="Acme Office Supplies", abn="12 345 678 901",
            invoice_number="DEMO-1001", invoice_date=today, due_date=today + timedelta(days=14),
            subtotal=Decimal("100.00"), gst=Decimal("10.00"), total=Decimal("110.00"),
            currency="AUD", confidence=0.92, confirmed=False,
        )

