import re

from app.processing.models import ExtractedDocument, PageContent


class TextCleaner:
    """Clean extracted PDF text."""

    def clean(
        self,
        document: ExtractedDocument,
    ) -> ExtractedDocument:
        cleaned_pages: list[PageContent] = []

        for page in document.pages:
            text = self._clean_text(page.text)

            cleaned_pages.append(
                PageContent(
                    page_number=page.page_number,
                    text=text,
                )
            )

        return ExtractedDocument(
            pages=cleaned_pages,
        )

    def _clean_text(
        self,
        text: str,
    ) -> str:
        text = text.replace("\r\n", "\n")
        text = text.replace("\r", "\n")

        # Collapse multiple spaces
        text = re.sub(r"[ \t]+", " ", text)

        # Collapse 3+ newlines into 2
        text = re.sub(r"\n{3,}", "\n\n", text)

        # Remove spaces before newlines
        text = re.sub(r" +\n", "\n", text)

        return text.strip()