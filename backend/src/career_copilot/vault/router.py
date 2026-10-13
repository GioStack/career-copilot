import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.models import SkillORM
from career_copilot.vault.schemas import Skill, SkillRead

router = APIRouter(prefix="/skills", tags=["skills"])


@router.post("", status_code=201)
def create_skill(skill: Skill, db: Annotated[Session, Depends(get_db)]) -> SkillRead:
    skill_orm = SkillORM(**skill.model_dump())
    db.add(skill_orm)
    db.commit()
    db.refresh(skill_orm)
    return SkillRead.model_validate(skill_orm)


@router.get("")
def list_skills(db: Annotated[Session, Depends(get_db)]) -> list[SkillRead]:
    skills = db.scalars(select(SkillORM)).all()
    return [SkillRead.model_validate(skill) for skill in skills]


@router.get("/{skill_id}")
def get_skill(skill_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> SkillRead:
    skill = db.get(SkillORM, skill_id)
    if skill is None:
        raise HTTPException(status_code=404, detail="Skill not found")

    return SkillRead.model_validate(skill)
