from app.processing.models import (
    ChunkedDocument,
    ExtractedDocument,
    TextChunk,
)


class TextChunker:
    """Split cleaned text into overlapping chunks."""

    def __init__(self, chunk_size: int = 1000, overlap: int = 200,) -> None:
        if overlap >= chunk_size:
            raise ValueError(
                "Overlap must be smaller than chunk size."
            )

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document: ExtractedDocument,) -> ChunkedDocument:
        chunks: list[TextChunk] = []
        chunk_number = 1

        step = self.chunk_size - self.overlap

        for page in document.pages:
            text = page.text

            for start in range(0, len(text), step):
                chunk_text = text[start : start + self.chunk_size]

                if not chunk_text.strip():
                    continue

                chunks.append(
                    TextChunk(
                        chunk_number=chunk_number,
                        page_number=page.page_number,
                        text=chunk_text,
                    )
                )
                chunk_number += 1

        return ChunkedDocument(
            chunks=chunks,
        )