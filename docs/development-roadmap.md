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
| 8 Hardening | Security, migrations, observability | Production readiness review passes | E2E/security/load |
| 9 Deploy/docs | CI/CD and operating guide | Repeatable deployment and support handoff | Deployment smoke test |

This run completes 0–4 and uses the existing mock review workflow for Phase 5. Tesseract mode currently supports PNG/JPEG invoices; PDF rendering is deferred. The dashboard includes only the four requested aggregates.
