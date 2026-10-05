# BizExpense

BizExpense is a portfolio-quality MVP for Australian SMEs to record expenses, upload invoices, review mock OCR results and see live spending totals. It deliberately keeps authentication, production OCR and accounting integrations out of scope.

## What works

- Expense create, filtered list/search, CSV export, view, edit and delete
- PDF/JPEG/PNG upload (10 MB limit) and replaceable Mock/Tesseract `OCRProvider`
- Mandatory user confirmation on the OCR review screen
- Database-backed dashboard totals, monthly spend, GST, count, category breakdown and six-month trend
- Seeded demo admin and ten expense categories
- FastAPI OpenAPI docs at `http://localhost:8000/docs`
- Alembic migration baseline, environment-based CORS and request/security headers
- Trusted-host enforcement and content-signature validation for PDF/JPEG/PNG uploads
- Authentication foundation with registration, PBKDF2 password hashing, JWT login and current-user lookup

## Local setup

Prerequisites: Python 3.11+, Node 20+, and Docker (for PostgreSQL).

```powershell
Copy-Item .env.example .env
docker compose up -d db
python -m venv backend/.venv
backend/.venv/Scripts/Activate.ps1
pip install -r backend/requirements-dev.txt
cd backend
python -m alembic upgrade head
cd ..
uvicorn app.main:app --reload --app-dir backend
```

In a second terminal:

```powershell
cd frontend
npm install
npm run dev
```

Open `http://localhost:5173`. The API reads `DATABASE_URL`, `CORS_ORIGINS` and `ALLOWED_HOSTS`. Development mode still creates missing tables for convenience; production mode requires `python -m alembic upgrade head` before startup. Every API response includes a request ID and baseline browser security headers. Uploads must have a permitted MIME type, matching extension and matching file signature.

Authentication endpoints are available at `/api/auth/register`, `/api/auth/login`, `/api/auth/refresh`, `/api/auth/logout` and `/api/auth/me`. Login and registration return a short-lived JWT access token plus a rotating opaque refresh token. Refresh tokens are stored only as SHA-256 hashes, can be revoked at logout, and cannot be reused after rotation. Set a strong `JWT_SECRET` in production; startup rejects the development default. Expense, supplier, dashboard, document and OCR endpoints require a Bearer token and isolate records by the authenticated user. The current MVP treats each user as one tenant; organization membership can be added later without accepting tenant IDs from clients.

The Web app redirects unauthenticated visitors to `/login`, supports registration, login and server-side sign-out, stores the access/refresh token pair in local storage for this prototype, and attaches the access token to API requests and CSV downloads. A shared API client performs one refresh-token rotation and retries the original request after an expired access token; failed refresh clears both tokens. For a higher-security production deployment, move the refresh token to a Secure, HttpOnly, SameSite cookie with an explicit CSRF design.

Runtime probes are available without authentication: `/api/health` is a lightweight liveness check, while `/api/health/ready` verifies the database connection and returns HTTP 503 when it is unavailable.

Authentication, document upload and OCR extraction endpoints use configurable per-client rate limits and return HTTP 429 with `Retry-After` when exceeded. Configure the shared window and endpoint limits with `RATE_LIMIT_WINDOW_SECONDS`, `AUTH_RATE_LIMIT_REQUESTS`, `UPLOAD_RATE_LIMIT_REQUESTS` and `OCR_RATE_LIMIT_REQUESTS`. The MVP limiter is process-local; a multi-worker deployment should replace its storage with a shared Redis-backed limiter.

Mock OCR is the default. The Tesseract integration supports PNG/JPEG directly and renders up to the first five pages of a PDF locally, combines their text, and averages page confidence before parsing; enable it with `OCR_PROVIDER=tesseract`. An optional OpenAI-compatible Vision provider supports PNG/JPEG input through `OCR_PROVIDER=vision`, `VISION_API_KEY`, `VISION_BASE_URL` and `VISION_MODEL`. Vision responses are validated for dates, non-negative amounts, GST/total consistency, currency, overall confidence and optional per-field confidence, always remain unconfirmed, and still require user review. Returned fields below 70% confidence are highlighted on the review page. Invoice images are sent to the configured provider, so its privacy, retention and billing terms must be reviewed before use. Broad layout validation and production accuracy against a representative real-invoice dataset remain deferred.

## Verification

```powershell
cd backend; python -m pytest -q; ruff check .
cd ../frontend; npm test; npm run build; npm run lint
```

The backend smoke suite verifies the primary demo path: registration, JWT authentication, expense creation, dashboard reconciliation, CSV export, document upload and OCR extraction.

See [docs/project-overview.md](docs/project-overview.md), [PROJECT_TASKS.md](PROJECT_TASKS.md), and the remaining `docs/` files for design decisions and future phases.
