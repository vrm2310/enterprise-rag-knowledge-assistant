from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.chunks.models import DocumentChunk


class ChunkRepository:
    """Repository for document chunks."""

    def __init__(self, db: Session,) -> None:
        self.db = db

    def create(self, chunk: DocumentChunk,) -> DocumentChunk:
        self.db.add(chunk)
        self.db.commit()
        self.db.refresh(chunk)

        return chunk

    # def create_many(self, chunks: list[DocumentChunk],) -> list[DocumentChunk]:
    #     self.db.add_all(chunks)
    #     self.db.commit()

    #     # for chunk in chunks:
    #     #     self.db.refresh(chunk)

    #     return chunks

    def create_many(
    self,
    chunks: list[DocumentChunk],
    ) -> list[DocumentChunk]:
        self.db.add_all(chunks)
        self.db.commit()

        # statement = select(DocumentChunk)
        #saved_chunks = self.db.scalars(statement).all()

        #print(f"Rows currently in document_chunks: {len(saved_chunks)}")

        # for chunk in saved_chunks:
        #     print(chunk.document_id, chunk.chunk_number)

        return chunks

    def get_by_document(self, document_id: UUID,) -> list[DocumentChunk]:
        statement = (
            select(DocumentChunk)
            .where(DocumentChunk.document_id == document_id)
            .order_by(DocumentChunk.chunk_number)
        )

        return list(self.db.scalars(statement).all())

    def delete_by_document(self, document_id: UUID,) -> None:
        chunks = self.get_by_document(document_id)

        for chunk in chunks:
            self.db.delete(chunk)

        self.db.commit()