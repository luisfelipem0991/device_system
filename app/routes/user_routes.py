from fastapi import APIRouter, Depends, Response, status, Query
from typing import List, Optional
from app.schemas.user_schema import UserCreate, UserResponse, UserUpdatePartial
from app.services.user_service import UserService
from app.dependencies.user_dependencies import get_user_or_404, verificar_correo_duplicado

router = APIRouter(prefix="/users", tags=["Users"])

# Tu función original de firmas con la actualización a la versión 2.0
def agregar_firmas_ocultas(response: Response):
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-API-Version"] = "2.0"

# GET: Listar todo y filtrar (Usa el servicio)
@router.get("/", response_model=List[UserResponse], status_code=status.HTTP_200_OK, summary="Listar y filtrar usuarios")
def obtener_usuarios(
    response: Response,
    role: Optional[str] = Query(None),
    is_active: Optional[bool] = Query(None)
):
    agregar_firmas_ocultas(response)
    return UserService.listar_usuarios(role, is_active)

# GET: Buscar por ID (Usa la inyección get_user_or_404)
@router.get("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Buscar usuario por ID")
def buscar_por_id(response: Response, usuario: dict = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    return usuario

# POST: Registrar Usuario (Inyecta la validación del correo)
@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED, summary="Registrar un nuevo usuario")
def crear_usuario(user_in: UserCreate, response: Response):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email)
    return UserService.crear_usuario(user_in)

# NUEVO PUT: Actualización completa
@router.put("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización completa de un usuario")
def actualizar_usuario_completo(user_in: UserCreate, response: Response, usuario: dict = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    verificar_correo_duplicado(user_in.email, excluir_id=usuario["id"])
    return UserService.actualizar_completo(usuario, user_in)

# NUEVO PATCH: Actualización parcial
@router.patch("/{user_id}", response_model=UserResponse, status_code=status.HTTP_200_OK, summary="Actualización parcial de un usuario")
def actualizar_usuario_parcial(user_in: UserUpdatePartial, response: Response, usuario: dict = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    if user_in.email:
        verificar_correo_duplicado(user_in.email, excluir_id=usuario["id"])
    return UserService.actualizar_parcial(usuario, user_in)

# NUEVO DELETE: Eliminar usuario (Retorna 204 No Content como pide la Fase 4)
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Eliminar un usuario del sistema")
def eliminar_usuario(response: Response, usuario: dict = Depends(get_user_or_404)):
    agregar_firmas_ocultas(response)
    UserService.eliminar_usuario(usuario)
    return Response(status_code=status.HTTP_204_NO_CONTENT)