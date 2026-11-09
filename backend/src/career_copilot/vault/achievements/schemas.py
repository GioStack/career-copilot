import uuid

from pydantic import BaseModel, ConfigDict, Field


class Achievement(BaseModel):
    """Achievement data sent by the client; the server sets the id, experience and position."""

    text: str = Field(min_length=1)


class AchievementRead(Achievement):
    """Achievement returned by the API, including the fields set by the server."""

    # Allows building from ORM objects: AchievementRead.model_validate(achievement_orm).
    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    experience_id: uuid.UUID
    position: int
