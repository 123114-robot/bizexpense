from pathlib import Path
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.models.document import UploadedDocument
from app.schemas.document import OCRResult
from app.services.ocr_service import OCRProcessingError, OCRProvider

ALLOWED_TYPES = {"application/pdf", "image/jpeg", "image/png"}
MAX_BYTES = 10 * 1024 * 1024


class DocumentService:
    def __init__(self, db: Session, upload_dir: Path):
        self.db = db
        self.upload_dir = upload_dir

    async def upload(self, file: UploadFile) -> UploadedDocument:
        if file.content_type not in ALLOWED_TYPES:
            raise HTTPException(415, "Only PDF, JPEG and PNG files are supported")
        content = await file.read(MAX_BYTES + 1)
        if len(content) > MAX_BYTES:
            raise HTTPException(413, "File exceeds the 10 MB limit")
        suffix = Path(file.filename or "document").suffix.lower()
        stored_name = f"{uuid4().hex}{suffix}"
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        path = self.upload_dir / stored_name
        path.write_bytes(content)
        document = UploadedDocument(
            filename=stored_name, original_filename=file.filename or "document",
            file_path=str(path), mime_type=file.content_type,
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def extract(self, document_id: int, provider: OCRProvider) -> OCRResult:
        document = self.db.get(UploadedDocument, document_id)
        if not document:
            raise HTTPException(404, "Document not found")
        try:
            return provider.extract(document.file_path)
        except OCRProcessingError as exc:
            raise HTTPException(422, str(exc)) from exc
