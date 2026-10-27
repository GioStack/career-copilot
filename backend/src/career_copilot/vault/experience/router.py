from typing import Annotated

from fastapi import APIRouter, Depends
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
