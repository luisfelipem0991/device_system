from pydantic import BaseModel, Field, EmailStr
from typing import Literal

# Las reglas básicas que todo usuario debe cumplir
class UserBase(BaseModel):
    name: str = Field(..., min_length=3)  # Nombre obligatorio y de mínimo 3 letras
    email: EmailStr                      # Correo con formato válido (que tenga @ y .com)
    role: Literal["admin", "support", "user"] # Solo se permiten estos 3 roles exactos
    is_active: bool = True               # Si no nos dicen nada, el usuario entra activo

# El molde para cuando vamos a CREAR un usuario (POST)
class UserCreate(UserBase):
    pass  # Usa las mismas reglas de arriba sin cambiar nada

# El molde para cuando la API RESPONDE con los datos (GET y POST)
class UserResponse(UserBase):
    id: int  # Le sumamos el ID que le asigna el sistema

    class Config:
        from_attributes = True  # Para que FastAPI no se enrede leyendo los datos