from fastapi import APIRouter, HTTPException, Query, Response, status
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["Users"])

# Nuestra "Base de datos" simulada (Con 3 usuarios iniciales)
db_users = [
    {"id": 1, "name": "Samuel Moreno", "email": "samuel@mail.com", "role": "admin", "is_active": True},
    {"id": 2, "name": "Andres Felipe", "email": "andres@mail.com", "role": "support", "is_active": True},
    {"id": 3, "name": "Carlos Gomez", "email": "carlos@mail.com", "role": "user", "is_active": False}
]

# Función para meter las dos firmas ocultas (Headers) que pide el taller
def agregar_firmas_ocultas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "1.0"

# POST: Registrar Usuario
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(user_in: UserCreate, response: Response):
    agregar_firmas_ocultas(response)
    
    # Revisar que el correo no esté repetido
    for usuario in db_users:
        if usuario["email"] == user_in.email:
            raise HTTPException(status_code=400, detail="Ese correo ya existe, intenta con otro.")
    
    # Crear un ID nuevo sumándole 1 al último de la lista
    nuevo_id = db_users[-1]["id"] + 1 if db_users else 1
    
    # Armar el usuario nuevo juntando el ID con los datos que nos mandaron
    nuevo_usuario = {"id": nuevo_id, **user_in.model_dump()}
    db_users.append(nuevo_usuario) # Guardarlo en la lista
    
    return nuevo_usuario

# GET: Listar todo y Filtrar
@router.get("/", response_model=List[UserResponse])
def obtener_usuarios(
    response: Response,
    role: Optional[str] = Query(None),       # Filtro opcional para buscar por rol (?role=...)
    is_active: Optional[bool] = Query(None)  # Filtro opcional para buscar por activo (?is_active=...)
):
    agregar_firmas_ocultas(response)
    resultado = db_users
    
    # Si el usuario escribe un rol en la URL, filtramos la lista
    if role is not None:
        resultado = [u for u in resultado if u["role"] == role.lower()]
        
    # Si el usuario escribe un estado en la URL, filtramos la lista
    if is_active is not None:
        resultado = [u for u in resultado if u["is_active"] == is_active]
        
    return resultado

# GET: Buscar por un ID específico
@router.get("/{user_id}", response_model=UserResponse)
def buscar_por_id(user_id: int, response: Response):
    agregar_firmas_ocultas(response)
    
    # Buscar el ID en la lista
    for usuario in db_users:
        if usuario["id"] == user_id:
            return usuario
            
    # Si termina el ciclo y no encontró nada, sacara el error 404
    raise HTTPException(status_code=404, detail="El usuario que buscas no existe.")