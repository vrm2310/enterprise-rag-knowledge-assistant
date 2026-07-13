from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.chunks.service import ChunkService
from app.core.storage import StorageService
from app.documents.enums import DocumentStatus
from app.documents.models import Document
from app.documents.repository import DocumentRepository
from app.processing.service import ProcessingService

#from backend.app import db


class DocumentService:
    """Business logic for document operations."""

    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)
        self.storage = StorageService()
        self.processing_service = ProcessingService()
        self.chunk_service = ChunkService(db)

    def create_document(self, document: Document,) -> Document:
        return self.repository.create(document)

    def get_document(self, document_id: UUID,) -> Document | None:
        return self.repository.get_by_id(document_id)

    def get_user_document(self, document_id: UUID, owner_id: UUID,) -> Document:
        document = self.repository.get_by_id(document_id)

        if document is None or document.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        return document

    def delete_user_document(self, document_id: UUID, owner_id: UUID,) -> None:
        document = self.repository.get_by_id(document_id)

        if document is None or document.owner_id != owner_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found.",
            )

        self.storage.delete_file(document.stored_filename)
        self.repository.delete(document)

    def upload_document(self, file: UploadFile, owner: User,) -> Document:
        self.storage.validate_pdf(file)
        stored_filename, _ = self.storage.save_file(file)

        document = Document(
            owner_id=owner.id,
            filename=file.filename or stored_filename,
            stored_filename=stored_filename,
            content_type=file.content_type or "application/pdf",
            file_size=file.size or 0,
            status=DocumentStatus.UPLOADED,
        )

        document = self.repository.create(document)

        self._process_uploaded_document(document)

        return document
    
    def _process_uploaded_document(self, document: Document,) -> None:
        #print("STEP 1: Entered _process_uploaded_document")

        pdf_path = self.storage.upload_dir / document.stored_filename
        #print(pdf_path)

        chunked_document = self.processing_service.process(pdf_path)
        #print(f"Chunks created: {chunked_document.total_chunks}")

        self.chunk_service.store_chunks(
            document.id,
            chunked_document,
        )

        #print("STEP 2: Chunks stored")