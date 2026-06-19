from fastapi import APIRouter, Depends, Response, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch, DeviceResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services.device_service import DeviceService
from app.services.loan_service import LoanService
from app.database.connection import get_db

router = APIRouter(prefix="/devices", tags=["Devices"])


@router.get(
    "/",
    response_model=List[DeviceResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar y filtrar dispositivos",
    description="Retorna dispositivos. Soporta filtros por `device_type`, `is_available`, `brand` y búsqueda libre con `search`.",
    response_description="Lista de dispositivos que cumplen los filtros."
)
def obtener_dispositivos(
    device_type: Optional[str] = Query(None, description="laptop, tablet, proyector, camara, router, monitor"),
    is_available: Optional[bool] = Query(None, description="Filtrar por disponibilidad"),
    brand: Optional[str] = Query(None, description="Filtrar por marca (búsqueda parcial)"),
    search: Optional[str] = Query(None, description="Búsqueda libre por nombre o número de serie"),
    db: Session = Depends(get_db)
):
    return DeviceService.listar_dispositivos(db, device_type, is_available, brand, search)


@router.get(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar dispositivo por ID",
    response_description="Dispositivo encontrado."
)
def buscar_por_id(device_id: int, db: Session = Depends(get_db)):
    return DeviceService.obtener_por_id(db, device_id)


@router.post(
    "/",
    response_model=DeviceResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo dispositivo",
    response_description="Dispositivo creado correctamente."
)
def crear_dispositivo(device_in: DeviceCreate, db: Session = Depends(get_db)):
    return DeviceService.crear_dispositivo(db, device_in)


@router.put(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa de un dispositivo"
)
def actualizar_completo(device_id: int, device_in: DeviceUpdate, db: Session = Depends(get_db)):
    return DeviceService.actualizar_completo(db, device_id, device_in)


@router.patch(
    "/{device_id}",
    response_model=DeviceResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de un dispositivo"
)
def actualizar_parcial(device_id: int, device_in: DevicePatch, db: Session = Depends(get_db)):
    return DeviceService.actualizar_parcial(db, device_id, device_in)


@router.delete(
    "/{device_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un dispositivo del sistema"
)
def eliminar_dispositivo(device_id: int, db: Session = Depends(get_db)):
    DeviceService.eliminar_dispositivo(db, device_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# GET /devices/{device_id}/loans — Historial de préstamos de un dispositivo (JOIN)
@router.get(
    "/{device_id}/loans",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar historial de préstamos de un dispositivo",
    description="Retorna todos los préstamos históricos asociados a un dispositivo, incluyendo datos del usuario.",
    response_description="Lista de préstamos del dispositivo con información relacionada."
)
def prestamos_del_dispositivo(device_id: int, db: Session = Depends(get_db)):
    return LoanService.prestamos_por_dispositivo(db, device_id)
