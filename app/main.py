from fastapi import FastAPI

app = FastAPI(
    title="HealthTrack AI",
    description=(
        "A demonstration clinical decision-support application. "
        "Outputs require review by a qualified healthcare professional."
    ),
    version="0.1.0",
)


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Report whether the application is running."""
    return {"status": "ok"}