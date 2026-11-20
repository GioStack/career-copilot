from fastapi import APIRouter, FastAPI

from career_copilot.vault.achievements.router import router as achievements_router
from career_copilot.vault.education.router import router as education_router
from career_copilot.vault.experience.router import router as experience_router
from career_copilot.vault.languages.router import router as languages_router
from career_copilot.vault.profile.router import router as profile_router
from career_copilot.vault.projects.router import router as projects_router
from career_copilot.vault.skills.router import router as skills_router

api_router = APIRouter(prefix="/api")
api_router.include_router(experience_router)
api_router.include_router(achievements_router)
api_router.include_router(skills_router)
api_router.include_router(profile_router)
api_router.include_router(languages_router)
api_router.include_router(projects_router)
api_router.include_router(education_router)


@api_router.get("/health")
def health() -> dict[str, str]:
    """Report that the server is running; does not check the database."""
    return {"status": "ok"}


app = FastAPI(title="Career Copilot")
app.include_router(api_router)
