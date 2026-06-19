from fastapi import FastAPI
from app.database.connection import engine, Base

# Importar todos los modelos para que SQLAlchemy registre sus tablas y relaciones
from app.models import user_model, device_model, loan_model  # noqa: F401

from app.routes import user_routes, device_routes, loan_routes

# Las tablas se gestionan con Alembic (alembic upgrade head), no con create_all.

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios, dispositivos y préstamos. "
        "Implementa SQLAlchemy ORM con relaciones (ForeignKey y relationship), "
        "migraciones controladas con Alembic y consultas avanzadas con joins y filtros."
    ),
    version="4.0.0",
    contact={"name": "Luis Felipe Molina"}
)

app.include_router(user_routes.router)
app.include_router(device_routes.router)
app.include_router(loan_routes.router)


@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "device_systems API v4.0 activa. Ve a /docs para explorar los endpoints."}
