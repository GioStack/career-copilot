
from fastapi import FastAPI

app = FastAPI(title="Career Copilot")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
