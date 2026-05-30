from fastapi import FastAPI
from app.routes import user_routes

# Inicializamos la aplicación de FastAPI
app = FastAPI(
    title="device_systems",
    description="Proyecto para gestionar usuarios del sistema",
    version="1.0"
)

# Conectamos las rutas de usuarios que escribimos en el otro archivo
app.include_router(user_routes.router)

# Pagina de bienvenida simple al entrar al link principal
@app.get("/", tags=["Inicio"])
def inicio():
    return {"mensaje": "Servidor corriendo. Entra a /docs para ver las pruebas."}