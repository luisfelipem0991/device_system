import os
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi.errors import RateLimitExceeded
from slowapi import _rate_limit_exceeded_handler

from app.database.connection import engine, Base

# Importar todos los modelos para que SQLAlchemy registre sus tablas y relaciones
from app.models import user_model, device_model, loan_model  # noqa: F401

from app.routes import user_routes, device_routes, loan_routes
from app.auth import auth_routes
from app.middlewares.request_middleware import RequestTracingMiddleware
from app.middlewares.rate_limiter import limiter

load_dotenv()

# Las tablas se gestionan con Alembic (alembic upgrade head), no con create_all.

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST segura para la gestión de usuarios, dispositivos y préstamos. "
        "Incluye autenticación OAuth2 con JWT, hash de contraseñas, autorización por roles, "
        "middleware de trazabilidad, CORS configurado y rate limiting."
    ),
    version="5.0.0",
    contact={"name": "Luis Felipe Molina"}
)

# --- Rate limiting (slowapi) ---
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# --- CORS ---
# En desarrollo solo se permiten orígenes locales conocidos.
# IMPORTANTE: no se debe usar allow_origins=["*"] junto con allow_credentials=True,
# ya que el navegador rechaza esa combinación y además expondría la API a cualquier
# dominio que quisiera enviar peticiones autenticadas (cookies o tokens) en nombre
# del usuario. Por eso se usa una lista blanca explícita de orígenes confiables.
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Middleware de trazabilidad personalizado ---
app.add_middleware(RequestTracingMiddleware)

# --- Routers ---
app.include_router(auth_routes.router)
app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)


@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "device_systems API v5.0 (segura) activa. Ve a /docs para explorar los endpoints."}


@app.get(
    "/security/policy",
    tags=["Security"],
    summary="Política de seguridad de la API",
    description="Resume los mecanismos de seguridad activos: hashing, JWT, CORS y límites de peticiones.",
    response_description="Resumen de la configuración de seguridad vigente."
)
def politica_de_seguridad():
    return {
        "autenticacion": "OAuth2 con JWT (Bearer token)",
        "hash_contraseñas": "bcrypt vía passlib",
        "cors_origenes_permitidos": cors_origins,
        "rate_limits": {
            "POST /auth/login": "5/minute",
            "POST /auth/register": "3/minute",
            "GET /users": "30/minute",
            "POST /loans": "10/minute"
        },
        "roles_soportados": ["admin", "support", "user"]
    }
