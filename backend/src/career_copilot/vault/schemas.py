import uuid

from pydantic import BaseModel, ConfigDict, Field


class Skill(BaseModel):
    name: str
    level: int = Field(ge=1, le=5)
    years: float | None = Field(default=None, ge=0, le=50)


class SkillRead(Skill):
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
