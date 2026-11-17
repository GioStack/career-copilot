import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class EducationORM(Base):
    """Database table for education; inheriting `Base` adds it to the metadata Alembic reads."""

    __tablename__ = "education"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    degree: Mapped[str]
    institution: Mapped[str]
    location: Mapped[str | None]
    start_date: Mapped[date]
    # Empty means still studying.
    end_date: Mapped[date | None]
    # From 0 to 10; checked by the API schema.
    grade: Mapped[float | None]
    description: Mapped[str | None]
