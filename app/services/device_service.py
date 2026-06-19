from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from fastapi import HTTPException, status
from app.models.device_model import Device
from app.schemas.device_schema import DeviceCreate, DeviceUpdate, DevicePatch


class DeviceService:

    @staticmethod
    def listar_dispositivos(
        db: Session,
        device_type: Optional[str] = None,
        is_available: Optional[bool] = None,
        brand: Optional[str] = None,
        search: Optional[str] = None
    ) -> List[Device]:
        query = db.query(Device)

        if device_type is not None:
            query = query.filter(Device.device_type == device_type.lower())

        if is_available is not None:
            query = query.filter(Device.is_available == is_available)

        if brand is not None:
            query = query.filter(Device.brand.ilike(f"%{brand}%"))

        if search is not None:
            query = query.filter(
                or_(
                    Device.name.ilike(f"%{search}%"),
                    Device.serial_number.ilike(f"%{search}%")
                )
            )

        return query.all()

    @staticmethod
    def obtener_por_id(db: Session, device_id: int) -> Device:
        dispositivo = db.query(Device).filter(Device.id == device_id).first()
        if not dispositivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El dispositivo que buscas no existe."
            )
        return dispositivo

    @staticmethod
    def verificar_serial_duplicado(db: Session, serial_number: str, excluir_id: Optional[int] = None):
        query = db.query(Device).filter(Device.serial_number == serial_number)
        if excluir_id is not None:
            query = query.filter(Device.id != excluir_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ese número de serie ya está registrado."
            )

    @staticmethod
    def crear_dispositivo(db: Session, device_in: DeviceCreate) -> Device:
        DeviceService.verificar_serial_duplicado(db, device_in.serial_number)
        nuevo = Device(**device_in.model_dump())
        db.add(nuevo)
        db.commit()
        db.refresh(nuevo)
        return nuevo

    @staticmethod
    def actualizar_completo(db: Session, device_id: int, datos: DeviceUpdate) -> Device:
        dispositivo = DeviceService.obtener_por_id(db, device_id)
        DeviceService.verificar_serial_duplicado(db, datos.serial_number, excluir_id=device_id)
        for campo, valor in datos.model_dump().items():
            setattr(dispositivo, campo, valor)
        db.commit()
        db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    def actualizar_parcial(db: Session, device_id: int, datos: DevicePatch) -> Device:
        dispositivo = DeviceService.obtener_por_id(db, device_id)
        campos_enviados = datos.model_dump(exclude_unset=True)

        if not campos_enviados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes enviar al menos un campo para actualizar."
            )

        if "serial_number" in campos_enviados:
            DeviceService.verificar_serial_duplicado(
                db, campos_enviados["serial_number"], excluir_id=device_id
            )

        for campo, valor in campos_enviados.items():
            setattr(dispositivo, campo, valor)

        db.commit()
        db.refresh(dispositivo)
        return dispositivo

    @staticmethod
    def eliminar_dispositivo(db: Session, device_id: int):
        dispositivo = DeviceService.obtener_por_id(db, device_id)
        db.delete(dispositivo)
        db.commit()
