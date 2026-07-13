from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings
from app.documents.exceptions import DocumentTooLargeError, UnsupportedFileTypeError

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

class StorageService:
    """Handles file storage operations."""

    def __init__(self) -> None:
        self.upload_dir = Path(settings.upload_dir)
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: UploadFile,) -> tuple[str, Path]:
        """
        Save uploaded file.
        Returns: (stored_filename, filepath)
        """

        extension = Path(file.filename or "").suffix

        stored_filename = f"{uuid4()}{extension}"

        filepath = self.upload_dir / stored_filename

        CHUNK_SIZE = 1024 * 1024  # 1 MB

        try:
            with filepath.open("wb") as buffer:
                while chunk := file.file.read(CHUNK_SIZE):
                    buffer.write(chunk)

        except Exception:
            if filepath.exists():
                filepath.unlink()
            raise

        return stored_filename, filepath
    
    def delete_file(self, stored_filename: str,) -> None:
        filepath = self.upload_dir / stored_filename

        if filepath.exists():
            filepath.unlink()

    def validate_pdf(self, file: UploadFile,) -> None:
        if not file.filename:
            raise UnsupportedFileTypeError("Filename is missing.")

        if not file.filename.lower().endswith(".pdf"):
            raise UnsupportedFileTypeError("Only PDF files are allowed.")

        if file.content_type != "application/pdf":
            raise UnsupportedFileTypeError("Only PDF files are allowed.")

        if file.size and file.size > MAX_FILE_SIZE:
            raise DocumentTooLargeError(
                f"Maximum upload size is {MAX_FILE_SIZE // (1024 * 1024)} MB."
            )