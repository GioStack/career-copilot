from sqlalchemy.orm import Mapped, mapped_column

from career_copilot.core.database import Base


class SkillORM(Base):
    __tablename__ = "skills"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    level: Mapped[int]
    years: Mapped[float | None]
