from app.embeddings.service import EmbeddingService


def test_embedding_generation() -> None:
    service = EmbeddingService()

    result = service.embed_text(
        "Enterprise RAG systems are awesome."
    )

    assert result.dimensions == 384

    assert len(result.embedding) == 384