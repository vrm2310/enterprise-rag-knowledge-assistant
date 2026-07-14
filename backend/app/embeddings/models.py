from pydantic import BaseModel


class EmbeddingResult(BaseModel):
    text: str
    embedding: list[float]

    @property
    def dimensions(self) -> int:
        return len(self.embedding)