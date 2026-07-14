from sentence_transformers import SentenceTransformer

from app.core.config import settings
from app.embeddings.exceptions import EmbeddingError
from app.embeddings.models import EmbeddingResult


class EmbeddingService:
    """Generate vector embeddings."""

    def __init__(self) -> None:
        self.model = SentenceTransformer(
            settings.embedding_model,
        )

    def embed_text(
        self,
        text: str,
    ) -> EmbeddingResult:
        """Generate an embedding for a single text."""

        try:
            embedding = self.model.encode(
                text,
                normalize_embeddings=True,
            )

            return EmbeddingResult(
                text=text,
                embedding=embedding.tolist(),
            )

        except Exception as err:
            raise EmbeddingError(
                "Failed to generate embedding."
            ) from err

    def embed_texts(
        self,
        texts: list[str],
    ) -> list[EmbeddingResult]:
        """Generate embeddings for multiple texts."""

        try:
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
            )

            return [
                EmbeddingResult(
                    text=text,
                    embedding=embedding.tolist(),
                )
                for text, embedding in zip(
                    texts,
                    embeddings,
                    strict=True,
                )
            ]

        except Exception as err:
            raise EmbeddingError(
                "Failed to generate embeddings."
            ) from err