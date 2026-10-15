from contextlib import asynccontextmanager

from fastapi import FastAPI

from career_copilot.core.database import Base, engine
from career_copilot.vault.router import router as vault_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Create missing tables on startup (see ADR 0007)."""
    Base.metadata.create_all(engine)
    yield


app = FastAPI(title="Career Copilot", lifespan=lifespan)
app.include_router(vault_router)


@app.get("/health")
def health() -> dict[str, str]:
    """Report that the server is running; does not check the database."""
    return {"status": "ok"}
