# Testing Strategy

Backend unit tests cover schema business rules and the OCR provider. API integration tests cover CRUD, confirmation persistence and dashboard aggregation using isolated SQLite. This differs from production PostgreSQL, so a later CI job should add PostgreSQL integration coverage.

Frontend tests cover form rendering, client validation, extracted field display and required confirmation. TypeScript build and lint provide static checks. Future work: upload integration tests, accessibility scans and Playwright browser workflows.

