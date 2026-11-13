import uuid

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class LanguageORM(Base):
    """Database table for languages; inheriting `Base` adds it to the metadata Alembic reads."""

    __tablename__ = "languages"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]

    # One of the CEFR levels (A1 to C2) or "Native"; checked by the API schema.
    level: Mapped[str]
