from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_model import BaseModel

if TYPE_CHECKING:
    from app.documents.models import Document


class DocumentChunk(BaseModel):
    __tablename__ = "document_chunks"

    document_id: Mapped[UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"),
        nullable=False,
    )

    chunk_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    page_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    document: Mapped["Document"] = relationship(
        back_populates="chunks",
    )