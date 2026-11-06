import uuid

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class SkillORM(Base):
    """Database table for skills; inheriting `Base` adds it to the metadata Alembic reads."""

    __tablename__ = "skills"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    level: Mapped[int]
    years: Mapped[float | None]
