# Development Roadmap

| Phase | Goal and tasks | Acceptance criteria | Tests |
|---|---|---|---|
| 0 Planning | Requirements and design | Docs reviewed and consistent | Document review |
| 1 Base setup | React, FastAPI, DB wiring | Both apps start locally | Health/smoke checks |
| 2 CRUD | Models, validation, services, UI | Full expense lifecycle | Schema and API CRUD |
| 3 Upload | Validate and store documents | Supported files persist | Upload edge cases |
| 4 OCR | Add Tesseract implementation | Real fields extracted with confidence | Provider fixtures |
| 5 Review | Harden confirmation workflow | Unconfirmed OCR cannot be finalized accidentally | UI/API workflow |
| 6 Analytics | Trends and category summaries | Metrics reconcile to ledger | Aggregate tests |
| 7 Search/export | Filters and CSV export | Results/export match filters | Query/export tests |
| 8A Foundation | Environment configuration, migrations, request tracing and response hardening | Migration round-trip and security-header tests pass | Integration/migration tests |
| 8B Perimeter | Trusted hosts and upload content verification | Spoofed hosts/files are rejected | Security integration/unit tests |
| 8C Identity | Authentication, tenant isolation, rate limits and security review | Production readiness review passes | E2E/security/load |
| 9 Deploy/docs | CI/CD and operating guide | Repeatable deployment and support handoff | Deployment smoke test |

This run completes the MVP workflow through Phase 8B. Tesseract mode currently supports PNG/JPEG invoices; PDF rendering is deferred. Production mode relies on Alembic rather than automatic table creation. Trusted hosts and upload signatures are enforced, while authentication, tenant isolation and rate limits remain Phase 8C work.
