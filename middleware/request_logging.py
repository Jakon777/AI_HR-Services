import logging
import time

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

log = logging.getLogger("ai_hr.api")


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Logs method, path, status, and duration for every HTTP request."""

    async def dispatch(self, request: Request, call_next):
        start = time.perf_counter()
        path = request.url.path
        method = request.method
        client = request.client.host if request.client else "-"

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            log.exception(
                "request failed | %s %s | client=%s | %.2fms",
                method,
                path,
                client,
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        log.info(
            "%s %s -> %s | client=%s | %.2fms",
            method,
            path,
            response.status_code,
            client,
            duration_ms,
        )
        return response
