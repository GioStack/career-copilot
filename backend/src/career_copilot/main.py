from fastapi import FastAPI

from career_copilot.vault.achievements.router import router as achievements_router
from career_copilot.vault.experience.router import router as experience_router
from career_copilot.vault.profile.router import router as profile_router
from career_copilot.vault.skills.router import router as skills_router

app = FastAPI(title="Career Copilot")
app.include_router(experience_router)
app.include_router(achievements_router)
app.include_router(skills_router)
app.include_router(profile_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the server is running; does not check the database."""
    return {"status": "ok"}
