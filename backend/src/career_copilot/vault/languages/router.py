from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.languages.models import LanguageORM
from career_copilot.vault.languages.schemas import Language, LanguageRead

router = APIRouter(prefix="/languages", tags=["languages"])


@router.post("", status_code=201)
def create_language(language: Language, db: Annotated[Session, Depends(get_db)]) -> LanguageRead:
    """Create a language and return it with its generated id."""
    language_orm = LanguageORM(**language.model_dump())
    db.add(language_orm)
    db.commit()
    db.refresh(language_orm)
    return LanguageRead.model_validate(language_orm)


@router.get("")
def list_languages(db: Annotated[Session, Depends(get_db)]) -> list[LanguageRead]:
    """Return all languages."""
    languages = db.scalars(select(LanguageORM)).all()
    return [LanguageRead.model_validate(language_orm) for language_orm in languages]
