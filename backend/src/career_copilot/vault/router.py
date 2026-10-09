from fastapi import APIRouter

from career_copilot.vault.schemas import Skill

router = APIRouter(prefix="/skills", tags=["skills"])

skills_db: list[Skill] = []


@router.post("", status_code=201)
def create_skill(skill: Skill) -> Skill:
    skills_db.append(skill)
    return skill


@router.get("")
def list_skills() -> list[Skill]:
    return skills_db
