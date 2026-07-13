from pathlib import Path
from typing import cast

import fitz

from app.processing.models import (
    ExtractedDocument,
    PageContent,
)


class PDFExtractor:
    """Extract text from PDF documents."""

    def extract(
        self,
        pdf_path: Path,
    ) -> ExtractedDocument:
        document = fitz.open(pdf_path)

        pages: list[PageContent] = []

        try:
            for page_number in range(document.page_count):
                page = document.load_page(page_number)

                text = cast(str, page.get_text("text")).strip()

                pages.append(
                    PageContent(
                        page_number=page_number + 1,
                        text=text,
                    )
                )

        finally:
            document.close()

        return ExtractedDocument(
            pages=pages,
        )