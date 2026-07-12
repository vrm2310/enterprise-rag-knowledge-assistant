from uuid import UUID

from sqlalchemy.orm import Session

from app.documents.models import Document
from app.documents.repository import DocumentRepository


class DocumentService:
    """Business logic for document operations."""

    def __init__(self, db: Session) -> None:
        self.repository = DocumentRepository(db)

    def create_document(
        self,
        document: Document,
    ) -> Document:
        return self.repository.create(document)

    def get_document(
        self,
        document_id: UUID,
    ) -> Document | None:
        return self.repository.get_by_id(document_id)

    def get_user_documents(
        self,
        owner_id: UUID,
    ) -> list[Document]:
        return self.repository.get_by_owner(owner_id)

    def delete_document(
        self,
        document: Document,
    ) -> None:
        self.repository.delete(document)