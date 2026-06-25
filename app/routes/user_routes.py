from fastapi import APIRouter, Depends, Request, Response, status, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.user_schema import UserUpdate, UserPatch, UserResponse
from app.schemas.loan_schema import LoanDetailResponse
from app.services.user_service import UserService
from app.services.loan_service import LoanService
from app.database.connection import get_db
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_active_user, require_admin
from app.middlewares.rate_limiter import limiter

router = APIRouter(prefix="/users", tags=["Users"])


def agregar_firmas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "5.0"


# GET /users — Listar con filtros opcionales (requiere autenticación)
@router.get(
    "/",
    response_model=List[UserResponse],
    status_code=status.HTTP_200_OK,
    summary="Listar y filtrar usuarios",
    description="Retorna todos los usuarios. Soporta filtros por `role`, `is_active` y orden por `name` o `created_at`. Requiere usuario autenticado. Límite: 30 solicitudes por minuto.",
    response_description="Lista de usuarios."
)
@limiter.limit("30/minute")
def obtener_usuarios(
    request: Request,
    response: Response,
    role: Optional[str] = Query(None, description="Filtrar por rol: admin, support, user"),
    is_active: Optional[bool] = Query(None, description="Filtrar por estado activo/inactivo"),
    order_by: Optional[str] = Query(None, description="Ordenar por: name, created_at"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agregar_firmas(response)
    return UserService.listar_usuarios(db, role, is_active, order_by)


# GET /users/{user_id} — Buscar por ID (requiere autenticación)
@router.get(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Buscar usuario por ID",
    description="Requiere usuario autenticado."
)
def buscar_por_id(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agregar_firmas(response)
    return UserService.obtener_por_id(db, user_id)


# PUT /users/{user_id} — Actualización completa (requiere admin)
@router.put(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización completa de un usuario",
    description="Requiere rol admin."
)
def actualizar_completo(
    user_id: int,
    user_in: UserUpdate,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    agregar_firmas(response)
    return UserService.actualizar_completo(db, user_id, user_in)


# PATCH /users/{user_id} — Actualización parcial (requiere admin)
@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    status_code=status.HTTP_200_OK,
    summary="Actualización parcial de un usuario",
    description="Requiere rol admin."
)
def actualizar_parcial(
    user_id: int,
    user_in: UserPatch,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    agregar_firmas(response)
    return UserService.actualizar_parcial(db, user_id, user_in)


# DELETE /users/{user_id} — Eliminar usuario (requiere admin)
@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Eliminar un usuario del sistema",
    description="Requiere rol admin."
)
def eliminar_usuario(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    agregar_firmas(response)
    UserService.eliminar_usuario(db, user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# GET /users/{user_id}/loans — Préstamos de un usuario (JOIN, requiere autenticación)
@router.get(
    "/{user_id}/loans",
    response_model=List[LoanDetailResponse],
    status_code=status.HTTP_200_OK,
    summary="Consultar préstamos de un usuario",
    description="Retorna todos los préstamos asociados a un usuario, incluyendo datos del dispositivo. Requiere usuario autenticado.",
    response_description="Lista de préstamos del usuario con información relacionada."
)
def prestamos_del_usuario(
    user_id: int,
    response: Response,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    agregar_firmas(response)
    return LoanService.prestamos_por_usuario(db, user_id)
