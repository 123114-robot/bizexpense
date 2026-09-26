from decimal import Decimal

from app.services.ocr_service import MockOCRProvider


def test_mock_ocr_returns_expected_structure():
    result = MockOCRProvider().extract("invoice.pdf")
    assert result.supplier_name == "Acme Office Supplies"
    assert result.total == Decimal("110.00")
    assert result.gst == Decimal("10.00")
    assert result.confidence == 0.92
    assert result.confirmed is False

