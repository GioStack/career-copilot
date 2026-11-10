import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.achievements.models import AchievementORM
from career_copilot.vault.achievements.schemas import Achievement, AchievementRead
from career_copilot.vault.experience.models import ExperienceORM

# No prefix: the paths start with /experiences/... here and /achievements/... later (ADR 0016).
router = APIRouter(tags=["achievements"])


@router.post("/experiences/{experience_id}/achievements", status_code=201)
def create_achievement(
    experience_id: uuid.UUID, achievement: Achievement, db: Annotated[Session, Depends(get_db)]
) -> AchievementRead:
    """Add an achievement at the next position of an experience, or 404 if it does not exist."""
    if db.get(ExperienceORM, experience_id) is None:
        raise HTTPException(status_code=404, detail="Experience not found")

    # The next position is one after the highest position of this experience.
    max_position = db.scalar(
        select(func.max(AchievementORM.position)).where(
            AchievementORM.experience_id == experience_id
        )
    )
    position = (max_position or 0) + 1

    achievement_orm = AchievementORM(
        experience_id=experience_id, position=position, **achievement.model_dump()
    )
    db.add(achievement_orm)
    db.commit()
    db.refresh(achievement_orm)
    return AchievementRead.model_validate(achievement_orm)


@router.get("/experiences/{experience_id}/achievements")
def list_achievements(
    experience_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> list[AchievementRead]:
    """Return the achievements of an experience in position order, or 404 if it does not exist."""
    if db.get(ExperienceORM, experience_id) is None:
        raise HTTPException(status_code=404, detail="Experience not found")
    achievements = db.scalars(
        select(AchievementORM)
        .where(AchievementORM.experience_id == experience_id)
        .order_by(AchievementORM.position)
    ).all()
    return [AchievementRead.model_validate(achievement_orm) for achievement_orm in achievements]


@router.get("/achievements/{achievement_id}")
def get_achievement(
    achievement_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]
) -> AchievementRead:
    """Return one achievement by id, or 404 if it does not exist."""
    achievement_orm = db.get(AchievementORM, achievement_id)
    if achievement_orm is None:
        raise HTTPException(status_code=404, detail="Achievement not found")

    return AchievementRead.model_validate(achievement_orm)
