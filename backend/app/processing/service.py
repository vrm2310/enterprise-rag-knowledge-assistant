from pathlib import Path

from app.processing.chunker import TextChunker
from app.processing.cleaner import TextCleaner
from app.processing.extractor import PDFExtractor
from app.processing.models import ChunkedDocument


class ProcessingService:
    """End-to-end PDF processing pipeline."""

    def __init__(self) -> None:
        self.extractor = PDFExtractor()
        self.cleaner = TextCleaner()
        self.chunker = TextChunker()

    def process(
        self,
        pdf_path: Path,
    ) -> ChunkedDocument:
        extracted = self.extractor.extract(pdf_path)

        cleaned = self.cleaner.clean(extracted)

        return self.chunker.chunk(cleaned)