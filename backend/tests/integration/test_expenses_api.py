from datetime import date


def expense_payload(**changes):
    payload = {
        "supplier_name": "Acme Office Supplies",
        "category_id": 1,
        "invoice_number": "INV-100",
        "invoice_date": "2026-09-02",
        "subtotal": "100.00",
        "gst_amount": "10.00",
        "total_amount": "110.00",
        "description": "Stationery",
        "ocr_confirmed": True,
    }
    payload.update(changes)
    return payload


def test_expense_crud(client):
    created = client.post("/api/expenses", json=expense_payload())
    assert created.status_code == 201
    expense_id = created.json()["id"]
    assert client.get(f"/api/expenses/{expense_id}").json()["description"] == "Stationery"
    updated = client.put(
        f"/api/expenses/{expense_id}", json=expense_payload(description="Updated")
    )
    assert updated.status_code == 200
    assert updated.json()["description"] == "Updated"
    assert len(client.get("/api/expenses").json()) == 1
    assert client.delete(f"/api/expenses/{expense_id}").status_code == 204
    assert client.get(f"/api/expenses/{expense_id}").status_code == 404


def test_dashboard_excludes_unconfirmed_ocr_drafts(client):
    current_date = date.today().isoformat()
    client.post("/api/expenses", json=expense_payload(invoice_date=current_date))
    client.post(
        "/api/expenses",
        json=expense_payload(
            supplier_name="Fuel Station",
            category_id=2,
            invoice_number="INV-101",
            subtotal="50",
            gst_amount="5",
            total_amount="55",
            invoice_date=current_date,
        ),
    )
    client.post(
        "/api/expenses",
        json=expense_payload(
            invoice_number="DRAFT-101",
            total_amount="220",
            subtotal="200",
            gst_amount="20",
            ocr_confirmed=False,
            invoice_date=current_date,
        ),
    )
    summary = client.get("/api/dashboard/summary")
    assert summary.status_code == 200
    assert summary.json()["total_expenses"] == "165.00"
    assert summary.json()["expenses_this_month"] == "165.00"
    assert summary.json()["gst_paid"] == "15.00"
    assert summary.json()["expense_count"] == 2
    assert summary.json()["category_breakdown"] == [
        {"category": "Office Supplies", "total": "110.00", "expense_count": 1},
        {"category": "Fuel", "total": "55.00", "expense_count": 1},
    ]
    assert len(summary.json()["monthly_trend"]) == 6
    assert summary.json()["monthly_trend"][-1] == {
        "month": date.today().strftime("%Y-%m"),
        "total": "165.00",
    }


def test_unconfirmed_ocr_expense_is_preserved_as_unconfirmed(client):
    created = client.post("/api/expenses", json=expense_payload(ocr_confirmed=False))
    assert created.status_code == 201
    assert created.json()["ocr_confirmed"] is False
