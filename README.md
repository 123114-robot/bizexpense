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

Mock OCR is the default. The Tesseract integration is a prototype with basic PNG/JPEG invoice-field parsing, not production-grade OCR. Enable it with `OCR_PROVIDER=tesseract`; Windows standard installs are detected automatically, otherwise set `TESSERACT_CMD`. Production accuracy, broad layout compatibility, PDF OCR, field-level confidence, cloud OCR and validation against a large real-invoice dataset are intentionally deferred.

## Verification

```powershell
cd backend; python -m pytest -q; ruff check .
cd ../frontend; npm test; npm run build; npm run lint
```

See [docs/project-overview.md](docs/project-overview.md), [PROJECT_TASKS.md](PROJECT_TASKS.md), and the remaining `docs/` files for design decisions and future phases.
