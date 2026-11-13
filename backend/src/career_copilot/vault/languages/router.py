import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
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


@router.get("/{language_id}")
def get_language(language_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> LanguageRead:
    """Return one language by id, or 404 if it does not exist."""
    language_orm = db.get(LanguageORM, language_id)
    if language_orm is None:
        raise HTTPException(status_code=404, detail="Language not found")

    return LanguageRead.model_validate(language_orm)


@router.put("/{language_id}")
def update_language(
    language_id: uuid.UUID, language: Language, db: Annotated[Session, Depends(get_db)]
) -> LanguageRead:
    """Replace a language's fields, or 404 if it does not exist."""
    language_orm = db.get(LanguageORM, language_id)
    if language_orm is None:
        raise HTTPException(status_code=404, detail="Language not found")

    # PUT replaces every field with the values from the request.
    for field, value in language.model_dump().items():
        setattr(language_orm, field, value)
    db.commit()
    db.refresh(language_orm)
    return LanguageRead.model_validate(language_orm)


@router.delete("/{language_id}", status_code=204)
def delete_language(language_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> None:
    """Delete a language, or 404 if it does not exist."""
    language_orm = db.get(LanguageORM, language_id)
    if language_orm is None:
        raise HTTPException(status_code=404, detail="Language not found")
    db.delete(language_orm)
    db.commit()
