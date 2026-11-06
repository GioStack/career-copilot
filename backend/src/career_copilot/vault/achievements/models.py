import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class AchievementORM(Base):
    """Database table for the achievements of a work experience (see ADR 0016)."""

    __tablename__ = "achievements"

    # Two achievements of the same experience cannot share a position.
    __table_args__ = (
        UniqueConstraint(
            "experience_id", "position", name="uq_achievements_experience_id_position"
        ),
    )

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    # PostgreSQL deletes the achievements when their experience is deleted.
    experience_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("experiences.id", ondelete="CASCADE")
    )
    text: Mapped[str]

    # Order within the experience: 1, 2, 3...
    position: Mapped[int]
