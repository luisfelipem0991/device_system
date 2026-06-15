from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional
from datetime import datetime


class UserBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre del usuario (mínimo 3 caracteres)")
    email: EmailStr = Field(..., description="Correo electrónico único y válido")
    role: Literal["admin", "support", "user"] = Field(..., description="Rol permitido: admin, support, user")
    is_active: bool = Field(True, description="Estado del usuario")


# Molde para CREAR (POST)
class UserCreate(UserBase):
    pass


# Molde para actualización COMPLETA (PUT) — reutiliza UserCreate
class UserUpdate(UserBase):
    pass


# Molde para actualización PARCIAL (PATCH) — todos los campos son opcionales
class UserPatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3, description="Nombre del usuario")
    email: Optional[EmailStr] = Field(None, description="Correo electrónico")
    role: Optional[Literal["admin", "support", "user"]] = Field(None, description="Rol del usuario")
    is_active: Optional[bool] = Field(None, description="Estado activo/inactivo")


# Mantener compatibilidad con el nombre anterior
UserUpdatePartial = UserPatch


# Molde de RESPUESTA — incluye id y created_at
class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
