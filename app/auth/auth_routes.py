from fastapi import APIRouter, Depends, Request, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas.auth_schema import UserRegister, UserLogin, Token, AuthUserResponse
from app.auth.auth_service import AuthService
from app.database.connection import get_db
from app.models.user_model import User
from app.dependencies.auth_dependency import get_current_active_user
from app.middlewares.rate_limiter import limiter

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post(
    "/register",
    response_model=AuthUserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un nuevo usuario",
    description=(
        "Crea un usuario con contraseña segura (mínimo 8 caracteres, con mayúscula, "
        "minúscula y número). La contraseña nunca se guarda en texto plano."
    ),
    response_description="Usuario registrado (sin datos sensibles)."
)
@limiter.limit("3/minute")
def registrar(request: Request, datos: UserRegister, db: Session = Depends(get_db)):
    return AuthService.registrar_usuario(db, datos)


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Iniciar sesión y obtener token JWT",
    description="Valida las credenciales y retorna un token de acceso Bearer. Recibe JSON (email y password).",
    response_description="Token de acceso JWT."
)
@limiter.limit("5/minute")
def login(request: Request, datos: UserLogin, db: Session = Depends(get_db)):
    usuario = AuthService.autenticar_usuario(db, datos)
    token = AuthService.generar_token(usuario)
    return Token(access_token=token, token_type="bearer")


@router.post(
    "/token",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login compatible con el botón Authorize de Swagger",
    description=(
        "Endpoint equivalente a /auth/login, pero recibe credenciales como formulario "
        "(username y password) en lugar de JSON, para ser compatible con el flujo "
        "OAuth2PasswordBearer que usa el botón 'Authorize' de Swagger UI. "
        "En el campo 'username' del formulario, ingresa tu correo electrónico."
    ),
    response_description="Token de acceso JWT.",
    include_in_schema=True
)
@limiter.limit("5/minute")
def login_form(request: Request, form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    datos = UserLogin(email=form_data.username, password=form_data.password)
    usuario = AuthService.autenticar_usuario(db, datos)
    token = AuthService.generar_token(usuario)
    return Token(access_token=token, token_type="bearer")


@router.get(
    "/me",
    response_model=AuthUserResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtener datos del usuario autenticado",
    description="Requiere token Bearer válido en la cabecera Authorization.",
    response_description="Datos del usuario autenticado, sin hashed_password."
)
def perfil_actual(current_user: User = Depends(get_current_active_user)):
    return current_user
