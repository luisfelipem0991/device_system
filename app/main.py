from fastapi import FastAPI
from app.routes import user_routes

app = FastAPI(
    title="device_systems API",
    description="API REST intermedia para la gestión avanzada del recurso usuarios, implementando patrones de arquitectura limpia, manejo de excepciones y Dependency Injection.",
    version="2.0.0",
    contact={
        "name": "Samuel Moreno"
    }
)

app.include_router(user_routes.router)

@app.get("/", tags=["Inicio"], include_in_schema=False)
def inicio():
    return {"mensaje": "Servidor de device_systems V2 activo. Dirígete a /docs"}