from decimal import Decimal

import pytest

from app.services.ocr_service import (
    MockOCRProvider,
    OCRProcessingError,
    TesseractOCRProvider,
    get_ocr_provider,
)


def test_mock_ocr_returns_expected_structure():
    result = MockOCRProvider().extract("invoice.pdf")
    assert result.supplier_name == "Acme Office Supplies"
    assert result.total == Decimal("110.00")
    assert result.gst == Decimal("10.00")
    assert result.confidence == 0.92
    assert result.confirmed is False


def test_tesseract_provider_parses_common_invoice_fields():
    text = """Acme Office Supplies
ABN 12 345 678 901
Invoice No: INV-204
Invoice Date: 15/09/2026
Due Date: 29/09/2026
Subtotal $100.00
GST $10.00
Total $110.00
"""
    provider = TesseractOCRProvider(engine=lambda _: (text, 87.5))

    result = provider.extract("invoice.png")

    assert result.supplier_name == "Acme Office Supplies"
    assert result.abn == "12 345 678 901"
    assert result.invoice_number == "INV-204"
    assert result.invoice_date.isoformat() == "2026-09-15"
    assert result.total == Decimal("110.00")
    assert result.confidence == 0.875
    assert result.confirmed is False


def test_tesseract_provider_rejects_pdf_before_running_engine():
    provider = TesseractOCRProvider(engine=lambda _: pytest.fail("engine should not run"))
    with pytest.raises(OCRProcessingError, match="PNG and JPEG"):
        provider.extract("invoice.pdf")


def test_provider_factory_uses_environment(monkeypatch):
    monkeypatch.setenv("OCR_PROVIDER", "tesseract")
    assert isinstance(get_ocr_provider(), TesseractOCRProvider)
