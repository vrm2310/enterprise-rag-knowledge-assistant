from pathlib import Path

from app.processing.service import ProcessingService


def test_processing_pipeline() -> None:
    service = ProcessingService()
    pdf = Path("tests/fixtures/sample.pdf")
    result = service.process(pdf)
    assert result.total_chunks > 0
    assert result.chunks[0].text