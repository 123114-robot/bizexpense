from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.document import DocumentRead, OCRResult
from app.services.document_service import DocumentService
from app.services.ocr_service import get_ocr_provider

router = APIRouter(prefix="/documents", tags=["documents"])
UPLOAD_DIR = Path(__file__).resolve().parents[2] / "uploads"


@router.post("/upload", response_model=DocumentRead, status_code=201)
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    return await DocumentService(db, UPLOAD_DIR).upload(file)


@router.post("/{document_id}/extract", response_model=OCRResult)
def extract_document(document_id: int, db: Session = Depends(get_db)):
    return DocumentService(db, UPLOAD_DIR).extract(document_id, get_ocr_provider())
