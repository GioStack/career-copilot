import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class ProjectORM(Base):
    """Database table for projects; inheriting `Base` adds it to the metadata Alembic reads."""

    __tablename__ = "projects"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]

    # A short summary, at most 500 characters; checked by the API schema.
    description: Mapped[str | None]

    # The database has no URL type, so the URL is stored as text.
    url: Mapped[str | None]

    start_date: Mapped[date | None]
    end_date: Mapped[date | None]
