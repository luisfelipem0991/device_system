from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_
from fastapi import HTTPException, status

from app.models.loan_model import Loan
from app.models.user_model import User
from app.models.device_model import Device
from app.schemas.loan_schema import LoanCreate


class LoanService:

    @staticmethod
    def obtener_por_id(db: Session, loan_id: int) -> Loan:
        prestamo = db.query(Loan).filter(Loan.id == loan_id).first()
        if not prestamo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El préstamo que buscas no existe."
            )
        return prestamo

    @staticmethod
    def crear_prestamo(db: Session, loan_in: LoanCreate) -> Loan:
        # Validar que el usuario exista
        usuario = db.query(User).filter(User.id == loan_in.user_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario indicado no existe."
            )

        # Validar que el dispositivo exista
        dispositivo = db.query(Device).filter(Device.id == loan_in.device_id).first()
        if not dispositivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El dispositivo indicado no existe."
            )

        # Validar que el dispositivo esté disponible
        if not dispositivo.is_available:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="El dispositivo no está disponible para préstamo."
            )

        nuevo_prestamo = Loan(
            user_id=loan_in.user_id,
            device_id=loan_in.device_id,
            loan_date=datetime.utcnow(),
            status="active"
        )
        dispositivo.is_available = False

        db.add(nuevo_prestamo)
        db.commit()
        db.refresh(nuevo_prestamo)
        return nuevo_prestamo

    @staticmethod
    def devolver_prestamo(db: Session, loan_id: int) -> Loan:
        prestamo = LoanService.obtener_por_id(db, loan_id)

        if prestamo.status == "returned":
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Este préstamo ya fue devuelto anteriormente."
            )

        prestamo.status = "returned"
        prestamo.return_date = datetime.utcnow()

        dispositivo = db.query(Device).filter(Device.id == prestamo.device_id).first()
        if dispositivo:
            dispositivo.is_available = True

        db.commit()
        db.refresh(prestamo)
        return prestamo

    @staticmethod
    def listar_prestamos(
        db: Session,
        status_filtro: Optional[str] = None,
        user_id: Optional[int] = None,
        device_id: Optional[int] = None
    ) -> List[Loan]:
        query = db.query(Loan)

        filtros = []
        if status_filtro is not None:
            filtros.append(Loan.status == status_filtro)
        if user_id is not None:
            filtros.append(Loan.user_id == user_id)
        if device_id is not None:
            filtros.append(Loan.device_id == device_id)

        if filtros:
            query = query.filter(and_(*filtros))

        return query.all()

    @staticmethod
    def listar_prestamos_con_detalle(
        db: Session,
        status_filtro: Optional[str] = None,
        user_email: Optional[str] = None,
        device_type: Optional[str] = None
    ) -> List[Loan]:
        """Consulta con JOIN entre loans, users y devices, con filtros opcionales."""
        query = (
            db.query(Loan)
            .join(User, Loan.user_id == User.id)
            .join(Device, Loan.device_id == Device.id)
            .options(joinedload(Loan.user), joinedload(Loan.device))
        )

        filtros = []
        if status_filtro is not None:
            filtros.append(Loan.status == status_filtro)
        if user_email is not None:
            filtros.append(User.email.ilike(f"%{user_email}%"))
        if device_type is not None:
            filtros.append(Device.device_type == device_type.lower())

        if filtros:
            query = query.filter(and_(*filtros))

        return query.all()

    @staticmethod
    def prestamos_por_usuario(db: Session, user_id: int) -> List[Loan]:
        usuario = db.query(User).filter(User.id == user_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario indicado no existe."
            )
        return (
            db.query(Loan)
            .options(joinedload(Loan.user), joinedload(Loan.device))
            .filter(Loan.user_id == user_id)
            .all()
        )

    @staticmethod
    def prestamos_por_dispositivo(db: Session, device_id: int) -> List[Loan]:
        dispositivo = db.query(Device).filter(Device.id == device_id).first()
        if not dispositivo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El dispositivo indicado no existe."
            )
        return (
            db.query(Loan)
            .options(joinedload(Loan.user), joinedload(Loan.device))
            .filter(Loan.device_id == device_id)
            .all()
        )
