import uuid
from datetime import date

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class ProfileORM(Base):
    """Database table for profiles; inheriting `Base` registers it for `create_all`."""

    __tablename__ = "profiles"

    # UUIDs instead of auto-increment ids (see ADR 0005).
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    full_name: Mapped[str]
    headline: Mapped[str]

    email: Mapped[str]
    phone: Mapped[str | None]
    location: Mapped[str | None]
    about: Mapped[str | None]

    # URLs are stored as plain text; the schema validates them.
    linkedin_url: Mapped[str | None]
    github_url: Mapped[str | None]
    portfolio_url: Mapped[str | None]

    birth_date: Mapped[date | None]
