import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.education.models import EducationORM
from career_copilot.vault.education.schemas import Education, EducationRead

router = APIRouter(prefix="/education", tags=["education"])


@router.post("", status_code=201)
def create_education(
    education: Education, db: Annotated[Session, Depends(get_db)]
) -> EducationRead:
    """Create an education entry and return it with its generated id."""
    education_orm = EducationORM(**education.model_dump())
    db.add(education_orm)
    db.commit()
    # Load the saved row explicitly, including any values set by the database.
    db.refresh(education_orm)
    return EducationRead.model_validate(education_orm)


@router.get("")
def list_education(db: Annotated[Session, Depends(get_db)]) -> list[EducationRead]:
    """Return all education entries, most recent start date first."""
    education = db.scalars(select(EducationORM).order_by(EducationORM.start_date.desc())).all()
    return [EducationRead.model_validate(education_orm) for education_orm in education]


@router.get("/{education_id}")
def get_education(
    education_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> EducationRead:
    """Return one education entry by id, or 404 if it does not exist."""
    education_orm = db.get(EducationORM, education_id)
    if education_orm is None:
        raise HTTPException(status_code=404, detail="Education not found")

    return EducationRead.model_validate(education_orm)


@router.put("/{education_id}")
def update_education(
    education_id: uuid.UUID, education: Education, db: Annotated[Session, Depends(get_db)]
) -> EducationRead:
    """Replace an education entry's fields, or 404 if it does not exist."""
    education_orm = db.get(EducationORM, education_id)
    if education_orm is None:
        raise HTTPException(status_code=404, detail="Education not found")

    # PUT replaces every field with the values from the request.
    for field, value in education.model_dump().items():
        setattr(education_orm, field, value)

    # No db.add(): the object was loaded by this session, so changes are tracked.
    db.commit()
    db.refresh(education_orm)
    return EducationRead.model_validate(education_orm)


@router.delete("/{education_id}", status_code=204)
def delete_education(education_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> None:
    education_orm = db.get(EducationORM, education_id)
    if education_orm is None:
        raise HTTPException(status_code=404, detail="Education not found")

    db.delete(education_orm)
    db.commit()
