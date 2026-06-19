from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime

DeviceType = Literal["laptop", "tablet", "proyector", "camara", "router", "monitor"]


class DeviceBase(BaseModel):
    name: str = Field(..., min_length=3, description="Nombre descriptivo del dispositivo")
    serial_number: str = Field(..., min_length=3, description="Número de serie único")
    device_type: DeviceType = Field(..., description="Tipo de dispositivo")
    brand: Optional[str] = Field(None, description="Marca del dispositivo (opcional)")
    is_available: bool = Field(True, description="Disponibilidad del dispositivo")


class DeviceCreate(DeviceBase):
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Laptop Lenovo ThinkPad",
                "serial_number": "LEN-2024-001",
                "device_type": "laptop",
                "brand": "Lenovo",
                "is_available": True
            }
        }


class DeviceUpdate(DeviceBase):
    pass


class DevicePatch(BaseModel):
    name: Optional[str] = Field(None, min_length=3)
    serial_number: Optional[str] = Field(None, min_length=3)
    device_type: Optional[DeviceType] = None
    brand: Optional[str] = None
    is_available: Optional[bool] = None


class DeviceResponse(DeviceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DeviceBasicInfo(BaseModel):
    """Versión reducida del dispositivo para mostrar dentro de un préstamo."""
    id: int
    name: str
    serial_number: str
    device_type: str

    class Config:
        from_attributes = True
