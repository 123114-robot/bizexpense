# Business Rules

- Subtotal, GST and total must be zero or greater; GST cannot exceed total.
- Currency defaults to AUD and dates must be valid ISO dates.
- Supplier, category, invoice date, description and monetary values are required.
- OCR output starts unconfirmed and is only final after explicit user confirmation.
- A single demo user owns all MVP expenses.
- Duplicate invoices do not block saving. A future warning will compare supplier, invoice number and total amount.

