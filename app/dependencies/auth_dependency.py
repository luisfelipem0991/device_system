from typing import List

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.models.user_model import User
from app.auth.security import decode_access_token

# El tokenUrl debe apuntar al endpoint que recibe el formulario OAuth2 (username/password),
# que es el que usa el botón "Authorize" de Swagger UI. El endpoint /auth/login con JSON
# sigue existiendo para clientes que no usan Swagger.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """Decodifica el token JWT y retorna el usuario autenticado. 401 si el token es inválido."""
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales.",
        headers={"WWW-Authenticate": "Bearer"}
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credenciales_invalidas

    user_id = payload.get("sub")
    if user_id is None:
        raise credenciales_invalidas

    usuario = db.query(User).filter(User.id == int(user_id)).first()
    if usuario is None:
        raise credenciales_invalidas

    return usuario


def get_current_active_user(current_user: User = Depends(get_current_user)) -> User:
    """Verifica que el usuario autenticado esté activo."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="El usuario está inactivo."
        )
    return current_user


def require_roles(roles_permitidos: List[str]):
    """Factory de dependencia: exige que el usuario autenticado tenga uno de los roles indicados."""
    def verificador(current_user: User = Depends(get_current_active_user)) -> User:
        if current_user.role not in roles_permitidos:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"No tienes permisos suficientes. Roles permitidos: {', '.join(roles_permitidos)}."
            )
        return current_user
    return verificador


# Dependencias listas para usar directamente en las rutas
require_admin = require_roles(["admin"])
require_admin_or_support = require_roles(["admin", "support"])
