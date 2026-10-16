import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ) -> Response:
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        logger.info(
            "Request completed",
            extra={
                "event": "request_completed",
                "request_id": request_id,
                "http_method": request.method,
                "http_path": request.url.path,
                "http_status": response.status_code,
            },
        )

        return response