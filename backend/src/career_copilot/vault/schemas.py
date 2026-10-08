from pydantic import BaseModel, Field


class Skill(BaseModel):
    name: str
    level: int = Field(ge=1, le=5)
    years: float | None = Field(default=None, ge=0, le=50)
