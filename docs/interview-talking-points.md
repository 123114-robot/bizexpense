# Interview Talking Points

- I chose a vertical slice that proves business value without over-building authentication or OCR.
- Validation exists at the API boundary and in database-oriented types; decimal values avoid floating-point money errors.
- The OCR interface uses dependency-friendly polymorphism, so a real engine can replace the mock without changing HTTP routes.
- Human confirmation is modelled explicitly because OCR confidence is not business correctness.
- Dashboard values are queries, not presentation constants, and integration tests reconcile totals.
- I would next add Alembic, PostgreSQL CI, authentication/tenant scoping, secure object storage and Tesseract fixtures.
- The key trade-off is startup table creation and local files for developer simplicity; neither is presented as production-ready.

