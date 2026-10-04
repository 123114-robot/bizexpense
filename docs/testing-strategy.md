# Testing Strategy

Backend unit tests cover schema business rules and the OCR provider. API integration tests cover CRUD, confirmation persistence and dashboard aggregation using isolated SQLite. This differs from production PostgreSQL, so a later CI job should add PostgreSQL integration coverage.

Frontend tests cover form rendering, client validation, extracted field display and required confirmation. TypeScript build and lint provide static checks. Future work: upload integration tests, accessibility scans and Playwright browser workflows.

## Development and CI workflow

During normal development, run only tests and checks related to the files being changed. Before requesting review, run the relevant package-level suite once. GitHub Actions is the authoritative full regression gate for pull requests to `main` and pushes to `main`:

- Backend: install `requirements-dev.txt`, run Ruff, then the complete Pytest suite.
- Frontend: run `npm ci`, ESLint, the complete Vitest suite, and `npm run build` (TypeScript checking plus the production Vite build).

No deployment workflow is configured because the project does not yet identify an actual deployment platform.

