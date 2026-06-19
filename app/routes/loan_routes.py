from fastapi import APIRouter, Depends, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.loan_schema import LoanCreate, LoanResponse, LoanDetailResponse
from app.services.loan_service import LoanService
from app.database.connection import get_db

router = APIRouter(prefix="/loans", tags=["Loans"])


@router.get(
    "/",
    response_model=List[LoanResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con filtros básicos",
    description="Filtra préstamos por `status`, `user_id` o `device_id`.",
    response_description="Lista de préstamos."
)
def listar_prestamos(
    status_filtro: Optional[str] = Query(None, alias="status", description="active, returned, overdue"),
    user_id: Optional[int] = Query(None, description="Filtrar por ID de usuario"),
    device_id: Optional[int] = Query(None, description="Filtrar por ID de dispositivo"),
    db: Session = Depends(get_db)
):
    return LoanService.listar_prestamos(db, status_filtro, user_id, device_id)


@router.get(
    "/details",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar préstamos con información de usuario y dispositivo (JOIN)",
    description=(
        "Realiza un JOIN entre `loans`, `users` y `devices`. "
        "Soporta filtros por `status`, `user_email` (búsqueda parcial) y `device_type`."
    ),
    response_description="Lista de préstamos con datos relacionados de usuario y dispositivo."
)
def listar_prestamos_con_detalle(
    status_filtro: Optional[str] = Query(None, alias="status", description="active, returned, overdue"),
    user_email: Optional[str] = Query(None, description="Filtrar por correo del usuario (búsqueda parcial)"),
    device_type: Optional[str] = Query(None, description="laptop, tablet, proyector, camara, router, monitor"),
    db: Session = Depends(get_db)
):
    return LoanService.listar_prestamos_con_detalle(db, status_filtro, user_email, device_type)


@router.get(
    "/{loan_id}",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar préstamo por ID"
)
def buscar_por_id(loan_id: int, db: Session = Depends(get_db)):
    return LoanService.obtener_por_id(db, loan_id)


@router.post(
    "/",
    response_model=LoanResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo préstamo",
    description=(
        "Crea un préstamo validando que el usuario y el dispositivo existan, "
        "y que el dispositivo esté disponible. Marca el dispositivo como no disponible."
    ),
    response_description="Préstamo creado correctamente."
)
def crear_prestamo(loan_in: LoanCreate, db: Session = Depends(get_db)):
    return LoanService.crear_prestamo(db, loan_in)


@router.patch(
    "/{loan_id}/return",
    response_model=LoanResponse,
    status_code=status.HTTP_200_OK,
    summary="Registrar la devolución de un préstamo",
    description="Marca el préstamo como `returned`, asigna fecha de devolución y libera el dispositivo.",
    response_description="Préstamo actualizado con estado returned."
)
def devolver_prestamo(loan_id: int, db: Session = Depends(get_db)):
    return LoanService.devolver_prestamo(db, loan_id)
