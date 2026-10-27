import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.experience.models import ExperienceORM
from career_copilot.vault.experience.schemas import Experience, ExperienceRead

router = APIRouter(prefix="/experiences", tags=["experiences"])


@router.post("", status_code=201)
def create_experience(
    experience: Experience, db: Annotated[Session, Depends(get_db)]
) -> ExperienceRead:
    """Create an experience and return it with its generated id."""
    experience_orm = ExperienceORM(**experience.model_dump())
    db.add(experience_orm)
    db.commit()
    # Load the saved row explicitly, including any values set by the database.
    db.refresh(experience_orm)
    return ExperienceRead.model_validate(experience_orm)


@router.get("")
def list_experiences(db: Annotated[Session, Depends(get_db)]) -> list[ExperienceRead]:
    """Return all experiences, most recent start date first."""
    experiences = db.scalars(select(ExperienceORM).order_by(ExperienceORM.start_date.desc())).all()
    return [ExperienceRead.model_validate(experience_orm) for experience_orm in experiences]


@router.get("/{experience_id}")
def get_experience(
    experience_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> ExperienceRead:
    """Return one experience by id, or 404 if it does not exist."""
    experience_orm = db.get(ExperienceORM, experience_id)
    if experience_orm is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    return ExperienceRead.model_validate(experience_orm)
