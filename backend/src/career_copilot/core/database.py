from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from career_copilot.core.config import settings

engine = create_engine(settings.database_url)

SessionLocal = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    """Registry of all ORM tables; used by `Base.metadata.create_all()`."""


def get_db() -> Generator[Session, None, None]:
    """Provide one session per request and always close it, even on errors."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
