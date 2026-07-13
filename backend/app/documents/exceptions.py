class DocumentError(Exception):
    """Base exception for document operations."""


class DocumentNotFoundError(DocumentError):
    """Raised when a document cannot be found."""


class UnsupportedFileTypeError(DocumentError):
    """Raised when an unsupported file type is uploaded."""


class DocumentTooLargeError(DocumentError):
    """Raised when uploaded file exceeds maximum size."""