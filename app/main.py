from fastapi import FastAPI

from app.api.routes import router

app = FastAPI(
    title="HealthTrack AI",
    description=(
        "AI-assisted clinical decision support for healthcare "
        "professionals. All outputs require qualified clinical review."
    ),
    version="0.2.0",
)

app.include_router(router)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Report whether the application is running."""

    return {"status": "ok"}
