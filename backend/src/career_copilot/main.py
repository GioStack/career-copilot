from fastapi import FastAPI

from career_copilot.vault.router import router as vault_router

app = FastAPI(title="Career Copilot")
app.include_router(vault_router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
