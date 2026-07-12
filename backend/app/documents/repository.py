from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.documents.models import Document


class DocumentRepository:
    """Repository for Document database operations."""

    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, document: Document) -> Document:
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document

    def get_by_id(self, document_id: UUID) -> Document | None:
        statement = select(Document).where(Document.id == document_id)
        return self.db.scalar(statement)

    def get_by_owner(self, owner_id: UUID) -> list[Document]:
        statement = (
            select(Document)
            .where(Document.owner_id == owner_id)
            .order_by(Document.created_at.desc())
        )
        return list(self.db.scalars(statement).all())

    def delete(self, document: Document) -> None:
        self.db.delete(document)
        self.db.commit()