import logging
import traceback
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.exc import SQLAlchemyError

logger = logging.getLogger(__name__)

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    """Global exception handler to ensure API always returns standard JSON."""
    async def dispatch(self, request: Request, call_next):
        try:
            return await call_next(request)
        except SQLAlchemyError as e:
            req_id = getattr(request.state, "req_id", "unknown")
            logger.error(f"[{req_id}] Database Error: {e}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Database Error",
                    "message": "A critical database operation failed.",
                    "request_id": req_id
                }
            )
        except Exception as e:
            req_id = getattr(request.state, "req_id", "unknown")
            logger.error(f"[{req_id}] Unhandled Exception: {e}\n{traceback.format_exc()}")
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal Server Error",
                    "message": "An unexpected error occurred in the MuseEngine.",
                    "request_id": req_id
                }
            )

async def global_exception_handler(request: Request, exc: Exception):
    req_id = getattr(request.state, "req_id", "unknown")
    logger.error(f"[{req_id}] Global Exception: {exc}\n{traceback.format_exc()}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "message": str(exc),
            "request_id": req_id
        }
    )

