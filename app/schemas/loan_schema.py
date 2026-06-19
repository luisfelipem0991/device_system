from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

LoanStatus = Literal["active", "returned", "overdue"]


class LoanCreate(BaseModel):
    user_id: int = Field(..., description="ID del usuario que solicita el préstamo")
    device_id: int = Field(..., description="ID del dispositivo a prestar")

    class Config:
        json_schema_extra = {
            "example": {"user_id": 1, "device_id": 3}
        }


class LoanUpdate(BaseModel):
    status: Optional[LoanStatus] = Field(None, description="Estado del préstamo")
    return_date: Optional[datetime] = Field(None, description="Fecha de devolución")


class LoanResponse(BaseModel):
    id: int
    user_id: int
    device_id: int
    loan_date: datetime
    return_date: Optional[datetime] = None
    status: LoanStatus

    class Config:
        from_attributes = True


# --- Schemas anidados para mostrar información relacionada (joins) ---

class UserBasicInfo(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True


class DeviceBasicInfo(BaseModel):
    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True


class LoanDetailResponse(BaseModel):
    """Respuesta enriquecida de un préstamo con datos de usuario y dispositivo."""
    loan_id: int = Field(..., alias="id")
    status: LoanStatus
    loan_date: datetime
    return_date: Optional[datetime] = None
    user: UserBasicInfo
    device: DeviceBasicInfo

    class Config:
        from_attributes = True
        populate_by_name = True
