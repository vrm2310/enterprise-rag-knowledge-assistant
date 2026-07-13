from uuid import UUID

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.auth.models import User
from app.core.storage import StorageService
from app.documents.enums import DocumentStatus
from app.documents.models import Document
from app.documents.repository import DocumentRepository


class DocumentService:
    """Business logic for document operations."""

    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)
        self.storage = StorageService()

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

        return self.repository.create(document)