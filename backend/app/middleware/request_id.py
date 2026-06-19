import uuid
import logging
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class RequestIDMiddleware(BaseHTTPMiddleware):
    """Injects a unique request ID into every API call for distributed tracing."""
    async def dispatch(self, request: Request, call_next):
        req_id = str(uuid.uuid4())
        # Attach to request state for access in endpoints
        request.state.req_id = req_id
        
        # Log the incoming request
        logger.debug(f"[{req_id}] Incoming request: {request.method} {request.url.path}")
        
        response = await call_next(request)
        
        # Inject into response headers
        response.headers["X-Request-ID"] = req_id
        return response

