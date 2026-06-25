import re
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


class UserRegister(BaseModel):
    """Schema de entrada para el registro de un nuevo usuario."""
    name: str = Field(..., min_length=3, description="Nombre completo del usuario")
    email: EmailStr = Field(..., description="Correo electrónico único")
    password: str = Field(
        ...,
        min_length=8,
        description="Contraseña segura: mínimo 8 caracteres, con mayúscula, minúscula y número"
    )
    role: Literal["admin", "support", "user"] = Field("user", description="Rol del usuario")

    @field_validator("password")
    @classmethod
    def validar_password_segura(cls, value: str) -> str:
        if " " in value:
            raise ValueError("La contraseña no puede contener espacios en blanco.")
        if not re.search(r"[A-Z]", value):
            raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
        if not re.search(r"[a-z]", value):
            raise ValueError("La contraseña debe contener al menos una letra minúscula.")
        if not re.search(r"\d", value):
            raise ValueError("La contraseña debe contener al menos un número.")
        return value

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Ana Perez",
                "email": "ana@sena.edu.co",
                "password": "Segura123",
                "role": "user"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema de entrada para el login."""
    email: EmailStr = Field(..., description="Correo electrónico registrado")
    password: str = Field(..., description="Contraseña en texto plano (se valida contra el hash)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {"email": "ana@sena.edu.co", "password": "Segura123"}
        }
    )


class Token(BaseModel):
    """Respuesta estándar de autenticación exitosa."""
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Datos extraídos del payload del token JWT."""
    user_id: Optional[int] = None
    email: Optional[EmailStr] = None
    role: Optional[str] = None


class AuthUserResponse(BaseModel):
    """Respuesta pública del usuario autenticado. Nunca incluye hashed_password."""
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
