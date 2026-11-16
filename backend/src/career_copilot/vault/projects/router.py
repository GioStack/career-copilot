import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from career_copilot.core.database import get_db
from career_copilot.vault.projects.models import ProjectORM
from career_copilot.vault.projects.schemas import Project, ProjectRead

router = APIRouter(prefix="/projects", tags=["projects"])


def to_columns(project: Project) -> dict[str, object]:
    """Return the project's fields as column values for the database."""
    columns = project.model_dump()
    # The database has no URL type, so the URL is stored as text.
    if columns["url"] is not None:
        columns["url"] = str(columns["url"])
    return columns


@router.post("", status_code=201)
def create_project(project: Project, db: Annotated[Session, Depends(get_db)]) -> ProjectRead:
    """Create a project and return it with its generated id."""
    project_orm = ProjectORM(**to_columns(project))
    db.add(project_orm)
    db.commit()
    # Load the saved row explicitly, including any values set by the database.
    db.refresh(project_orm)
    return ProjectRead.model_validate(project_orm)


@router.get("")
def list_projects(db: Annotated[Session, Depends(get_db)]) -> list[ProjectRead]:
    """Return all projects."""
    projects = db.scalars(select(ProjectORM)).all()
    return [ProjectRead.model_validate(project_orm) for project_orm in projects]


@router.get("/{project_id}")
def get_project(project_id: uuid.UUID, db: Annotated[Session, Depends(get_db)]) -> ProjectRead:
    """Return one project by id, or 404 if it does not exist."""
    project_orm = db.get(ProjectORM, project_id)
    if project_orm is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return ProjectRead.model_validate(project_orm)
