from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta
from decimal import Decimal
import os
from pathlib import Path
import re
from typing import Callable

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


class OCRProcessingError(RuntimeError):
    """Raised when a document cannot be processed by the selected OCR provider."""


class TesseractOCRProvider(OCRProvider):
    def __init__(self, engine: Callable[[str], tuple[str, float]] | None = None):
        self.engine = engine or self._run_tesseract

    def extract(self, file_path: str) -> OCRResult:
        if Path(file_path).suffix.lower() not in {".png", ".jpg", ".jpeg"}:
            raise OCRProcessingError("Tesseract OCR currently supports PNG and JPEG invoices only")
        try:
            text, confidence_percent = self.engine(file_path)
        except OCRProcessingError:
            raise
        except Exception as exc:
            raise OCRProcessingError(f"Tesseract OCR failed: {exc}") from exc
        return self._parse(text, confidence_percent)

    @staticmethod
    def _run_tesseract(file_path: str) -> tuple[str, float]:
        try:
            import pytesseract
            from PIL import Image
        except ImportError as exc:
            raise OCRProcessingError("Install pytesseract and Pillow to use Tesseract OCR") from exc
        configured_command = os.getenv("TESSERACT_CMD")
        windows_command = Path(r"C:\Program Files\Tesseract-OCR\tesseract.exe")
        if configured_command:
            pytesseract.pytesseract.tesseract_cmd = configured_command
        elif windows_command.exists():
            pytesseract.pytesseract.tesseract_cmd = str(windows_command)
        try:
            data = pytesseract.image_to_data(Image.open(file_path), output_type=pytesseract.Output.DICT)
        except pytesseract.TesseractNotFoundError as exc:
            raise OCRProcessingError("Tesseract executable is not installed or not on PATH") from exc
        lines: dict[tuple[int, int, int], list[str]] = {}
        for index, raw_word in enumerate(data["text"]):
            word = raw_word.strip()
            if word:
                key = (data["block_num"][index], data["par_num"][index], data["line_num"][index])
                lines.setdefault(key, []).append(word)
        confidences = [float(value) for value in data["conf"] if float(value) >= 0]
        confidence = sum(confidences) / len(confidences) if confidences else 0.0
        return "\n".join(" ".join(words) for words in lines.values()), confidence

    @staticmethod
    def _parse(text: str, confidence_percent: float) -> OCRResult:
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        def match(pattern: str) -> str | None:
            result = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
            return result.group(1).strip() if result else None

        def money(label: str) -> Decimal:
            value = match(rf"^{label}\s*[:$]?\s*\$?([\d,]+\.\d{{2}})")
            return Decimal(value.replace(",", "")) if value else Decimal("0.00")

        def parsed_date(label: str) -> date | None:
            value = match(rf"{label}\s*:?\s*(\d{{1,2}}[/-]\d{{1,2}}[/-]\d{{4}}|\d{{4}}-\d{{2}}-\d{{2}})")
            if not value:
                return None
            for format_string in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d"):
                try:
                    return date.fromisoformat(value) if format_string == "%Y-%m-%d" else datetime.strptime(value, format_string).date()
                except ValueError:
                    continue
            return None

        return OCRResult(
            supplier_name=lines[0] if lines else "Unknown supplier",
            abn=match(r"\bABN\s*:?\s*([\d ]{11,14})"),
            invoice_number=match(r"Invoice\s*(?:No\.?|Number|#)\s*:?\s*([A-Z0-9-]+)"),
            invoice_date=parsed_date(r"Invoice\s+Date") or date.today(),
            due_date=parsed_date(r"Due\s+Date"),
            subtotal=money("Subtotal"),
            gst=money("GST"),
            total=money("Total"),
            currency="AUD",
            confidence=max(0.0, min(confidence_percent / 100, 1.0)),
            confirmed=False,
        )


def get_ocr_provider() -> OCRProvider:
    provider = os.getenv("OCR_PROVIDER", "mock").lower()
    if provider == "tesseract":
        return TesseractOCRProvider()
    return MockOCRProvider()
