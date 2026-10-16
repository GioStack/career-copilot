import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.skills.models import SkillORM
from career_copilot.vault.skills.schemas import Skill, SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", status_code=201)
def create_skill(skill: Skill, db: Annotated[Session, Depends(get_db)]) -> SkillRead:
    """Create a skill and return it with its generated id."""
    skill_orm = SkillORM(**skill.model_dump())
    db.add(skill_orm)
    db.commit()
    # Load the saved row explicitly, including any values set by the database.
    db.refresh(skill_orm)
    return SkillRead.model_validate(skill_orm)


@router.get("")
def list_skills(db: Annotated[Session, Depends(get_db)]) -> list[SkillRead]:
    """Return all skills."""
    skills = db.scalars(select(SkillORM)).all()
    return [SkillRead.model_validate(skill) for skill in skills]


@router.get("/{skill_id}")
def get_skill(skill_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> SkillRead:
    """Return one skill by id, or 404 if it does not exist."""
    skill = db.get(SkillORM, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    return SkillRead.model_validate(skill)


@router.put("/{skill_id}")
def update_skill(
    skill_id: uuid.UUID, skill: Skill, db: Annotated[Session, Depends(get_db)]
) -> SkillRead:
    """Replace a skill's fields, or 404 if it does not exist."""
    skill_orm = db.get(SkillORM, skill_id)
    if skill_orm is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    # PUT replaces every field with the values from the request.
    for field, value in skill.model_dump().items():
        setattr(skill_orm, field, value)

    # No db.add(): the object was loaded by this session, so changes are tracked.
    db.commit()
    db.refresh(skill_orm)
    return SkillRead.model_validate(skill_orm)


@router.delete("/{skill_id}", status_code=204)
def delete_skill(skill_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> None:
    """Delete a skill, or 404 if it does not exist."""
    skill_orm = db.get(SkillORM, skill_id)
    if skill_orm is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    db.delete(skill_orm)
    db.commit()
