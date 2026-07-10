from app.db.base import Base
from app.db.mixins import TimestampMixin, UUIDMixin


class BaseModel(Base, UUIDMixin, TimestampMixin):
    __abstract__ = True