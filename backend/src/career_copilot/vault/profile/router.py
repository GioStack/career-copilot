from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from pydantic import HttpUrl
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.profile.models import ProfileORM
from career_copilot.vault.profile.schemas import Profile, ProfileRead

router = APIRouter(prefix="/profile", tags=["profiles"])


@router.get("")
def get_profile(db: Annotated[Session, Depends(get_db)]) -> ProfileRead:
    """Return the profile, or 404 if it has not been created yet."""
    profile_orm = db.scalars(select(ProfileORM)).first()

    if profile_orm is None:
        raise HTTPException(status_code=404, detail="Profile not found")

    return ProfileRead.model_validate(profile_orm)


# PUT, not POST: there is only one profile, so each call saves over it
# (creates it the first time, replaces it afterwards).
@router.put("")
def put_profile(profile: Profile, db: Annotated[Session, Depends(get_db)]) -> ProfileRead:
    """Create the profile, or replace it if it already exists."""
    profile_orm = db.scalars(select(ProfileORM)).first()

    if profile_orm is None:
        profile_orm = ProfileORM()
        # New object: add it to the session so commit() saves it.
        db.add(profile_orm)

    for field, value in profile.model_dump().items():
        # SQLite has no URL type, so URLs are stored as text.
        if isinstance(value, HttpUrl):
            value = str(value)
        setattr(profile_orm, field, value)

    db.commit()
    db.refresh(profile_orm)
    return ProfileRead.model_validate(profile_orm)
