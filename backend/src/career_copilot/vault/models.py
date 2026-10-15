import uuid

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class SkillORM(Base):
    """Database table for skills; inheriting `Base` registers it for `create_all`."""

    __tablename__ = "skills"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    level: Mapped[int]
    years: Mapped[float | None]
