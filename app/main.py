from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from app.api.routes import router
from app.api.auth_routes import router as auth_router
from app.core.logging_config import configure_logging
from app.core.request_middleware import RequestIDMiddleware
import logging

configure_logging()

app = FastAPI(
    title="HealthTrack AI",
    description=(
        "AI-assisted clinical decision support for healthcare "
        "professionals. All outputs require qualified clinical review."
    ),
    version="0.3.0",
)
app.add_middleware(RequestIDMiddleware)
templates = Jinja2Templates(directory="app/templates")

app.include_router(router)
app.include_router(auth_router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the HealthTrack AI homepage."""
    return templates.TemplateResponse(
        request=request,
        name="index.html",
    )


@app.get("/api/health")
async def health_check() -> dict[str, str]:
    """Report whether the application is running."""
    return {"status": "ok"}

@app.get("/api/log-test")
async def log_test() -> dict[str, str]:
    """Verify that structured logging is configured."""
    logger = logging.getLogger(__name__)
    logger.info(
        "Structured logging test event",
        extra={"event": "logging_test"},
    )
    return {"status": "logging test recorded"}