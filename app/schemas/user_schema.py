from pydantic import BaseModel, Field, EmailStr
from typing import Literal, Optional

# Tus reglas básicas originales (Se quedan tal cual)
class UserBase(BaseModel):
    name: str = Field(..., min_length=3)
    email: EmailStr
    role: Literal["admin", "support", "user"]
    is_active: bool = True

# Molde para CREAR (POST) y para actualización COMPLETA (PUT)
class UserCreate(UserBase):
    pass

# NUEVO CAMBIO EV08: Molde para actualización PARCIAL (PATCH)
# Todos los campos se vuelven opcionales usando Optional
class UserUpdatePartial(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    email: Optional[EmailStr] = None
    role: Optional[Literal["admin", "support", "user"]] = None
    is_active: Optional[bool] = None

# Tu molde de RESPUESTA original (Se queda tal cual)
class UserResponse(UserBase):
    id: int

    class Config:
        from_attributes = True