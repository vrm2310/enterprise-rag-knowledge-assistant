from uuid import UUID

from sqlalchemy.orm import Session

from app.chunks.models import DocumentChunk
from app.chunks.repository import ChunkRepository
from app.processing.models import ChunkedDocument


class ChunkService:
    """Persist and retrieve document chunks."""

    def __init__(
        self,
        db: Session,
    ) -> None:
        self.repository = ChunkRepository(db)

    def store_chunks(
        self,
        document_id: UUID,
        chunked_document: ChunkedDocument,
    ) -> list[DocumentChunk]:
        chunks = [
            DocumentChunk(
                document_id=document_id,
                chunk_number=chunk.chunk_number,
                page_number=chunk.page_number,
                text=chunk.text,
            )
            for chunk in chunked_document.chunks
        ]

        return self.repository.create_many(chunks)

    def get_document_chunks(
        self,
        document_id: UUID,
    ) -> list[DocumentChunk]:
        return self.repository.get_by_document(document_id)