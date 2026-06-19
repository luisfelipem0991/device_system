from fastapi import APIRouter, Depends, Response, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserCreate, UserUpdate, UserPatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.database.connection import get_db

router = APIRouter(prefix="/users", tags=["Users"])


def agregar_firmas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "3.0"


# GET /users — Listar con filtros opcionales
@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar y filtrar usuarios",
    description="Retorna todos los usuarios. Soporta filtros por `role`, `is_active` y orden por `name` o `created_at`."
)
def obtener_usuarios(
    response: Response,
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query(None, description="Ordenar por: name, created_at"),
    db: Session = Depends(get_db)
):
    agregar_firmas(response)
    return UserService.listar_usuarios(db, role, is_active, order_by)


# GET /users/{user_id} — Buscar por ID
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuario por ID"
)
def buscar_por_id(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    return UserService.obtener_por_id(db, user_id)


# POST /users — Crear usuario
@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario"
)
def crear_usuario(user_in: UserCreate, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    return UserService.crear_usuario(db, user_in)


# PUT /users/{user_id} — Actualización completa
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa de un usuario"
)
def actualizar_completo(user_id: int, user_in: UserUpdate, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    return UserService.actualizar_completo(db, user_id, user_in)


# PATCH /users/{user_id} — Actualización parcial
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de un usuario"
)
def actualizar_parcial(user_id: int, user_in: UserPatch, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    return UserService.actualizar_parcial(db, user_id, user_in)


# DELETE /users/{user_id} — Eliminar usuario
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario del sistema"
)
def eliminar_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    UserService.eliminar_usuario(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# GET /users/{user_id}/loans — Préstamos de un usuario (JOIN)
@router.get(
    "/{user_id}/loans",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar préstamos de un usuario",
    description="Retorna todos los préstamos asociados a un usuario, incluyendo datos del dispositivo.",
    response_description="Lista de préstamos del usuario con información relacionada."
)
def prestamos_del_usuario(user_id: int, response: Response, db: Session = Depends(get_db)):
    agregar_firmas(response)
    return LoanService.prestamos_por_usuario(db, user_id)
