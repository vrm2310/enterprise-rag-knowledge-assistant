from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.documents.enums import DocumentStatus


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    content_type: str
    file_size: int
    status: DocumentStatus
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)