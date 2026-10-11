import uuid

from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class SkillORM(Base):
    __tablename__ = "skills"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    level: Mapped[int]
    years: Mapped[float | None]
