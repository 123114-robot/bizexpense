# Database Design

`User 1—* Expense *—1 Supplier`, `Expense *—1 ExpenseCategory`, and `Expense 0..1—0..1 UploadedDocument`.

Amounts use `NUMERIC(12,2)`, dates use `DATE`, and audit timestamps are database-generated. Supplier reuse currently matches exact names. The application creates tables at startup for MVP convenience; production should use Alembic migrations. Indexes exist on user email and supplier name. Future duplicate detection should use a normalized supplier key plus invoice number and total.

