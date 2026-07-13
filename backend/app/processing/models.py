from pydantic import BaseModel


class TextChunk(BaseModel):
    chunk_number: int
    page_number: int
    text: str

    @property
    def character_count(self) -> int:
        return len(self.text)


class ChunkedDocument(BaseModel):
    chunks: list[TextChunk]

    @property
    def total_chunks(self) -> int:
        return len(self.chunks)


class PageContent(BaseModel):
    page_number: int
    text: str


class ExtractedDocument(BaseModel):
    pages: list[PageContent]

    @property
    def full_text(self) -> str:
        return "\n\n".join(
            page.text
            for page in self.pages
        )

    @property
    def total_pages(self) -> int:
        return len(self.pages)

    @property
    def total_characters(self) -> int:
        return sum(
            len(page.text)
            for page in self.pages
        )