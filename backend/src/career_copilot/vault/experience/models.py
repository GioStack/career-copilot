import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class ExperienceORM(Base):
    """Database table for experiences; inheriting `Base` registers it for `create_all`."""

    __tablename__ = "experiences"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    title: Mapped[str]
    company: Mapped[str]
    location: Mapped[str | None]
    start_date: Mapped[date]

    # Empty means the current position.
    end_date: Mapped[date | None]

    description: Mapped[str | None]
