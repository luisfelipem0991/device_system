from fastapi import FastAPI
from app.database.connection import engine, Base
from app.models import user_model  # noqa: F401 — necesario para registrar los modelos
from app.routes import user_routes

# Crea las tablas en la BD si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="device_systems API",
    description=(
        "API REST para la gestión de usuarios con persistencia en base de datos SQLite. "
        "Implementa patrones de arquitectura limpia, SQLAlchemy ORM, manejo de errores y Dependency Injection."
    ),
    version="3.0.0",
    contact={"name": "Luis Felipe Molina"}
)

app.include_router(user_routes.router)


@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "device_systems API v3.0 activa. Ve a /docs para explorar los endpoints."}
