import time
import uuid
import logging

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request

logger = logging.getLogger("device_systems")
logging.basicConfig(level=logging.INFO)


class RequestTracingMiddleware(BaseHTTPMiddleware):
    """
    Middleware global que:
    - Mide el tiempo de respuesta de cada petición.
    - Agrega la cabecera X-Process-Time.
    - Agrega la cabecera X-App-Name.
    - Genera o propaga un X-Request-ID para trazabilidad.
    - Registra método, ruta y código de estado en el log.
    """

    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4())[:8])
        inicio = time.time()

        response = await call_next(request)

        duracion = time.time() - inicio
        response.headers["X-App-Name"] = "device_systems"
        response.headers["X-Process-Time"] = f"{duracion:.4f}"
        response.headers["X-Request-ID"] = request_id

        logger.info(
            f"[{request_id}] {request.method} {request.url.path} -> "
            f"{response.status_code} ({duracion:.4f}s)"
        )

        return response
