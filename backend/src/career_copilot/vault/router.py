from typing import Annotated

from fastapi import APIRouter, Depends
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
