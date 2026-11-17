from typing import Annotated

from fastapi import APIRouter, Depends
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
