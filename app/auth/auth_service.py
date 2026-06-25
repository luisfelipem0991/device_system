from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user_model import User
from app.schemas.auth_schema import UserRegister, UserLogin
from app.auth.security import get_password_hash, verify_password, create_access_token


class AuthService:

    @staticmethod
    def registrar_usuario(db: Session, datos: UserRegister) -> User:
        """Registra un usuario nuevo con contraseña hasheada."""
        existente = db.query(User).filter(User.email == datos.email).first()
        if existente:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ese correo ya está registrado."
            )

        nuevo_usuario = User(
            name=datos.name,
            email=datos.email,
            hashed_password=get_password_hash(datos.password),
            role=datos.role,
            is_active=True
        )
        db.add(nuevo_usuario)
        db.commit()
        db.refresh(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def autenticar_usuario(db: Session, datos: UserLogin) -> User:
        """Valida credenciales y retorna el usuario si son correctas."""
        usuario = db.query(User).filter(User.email == datos.email).first()

        credenciales_invalidas = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Correo o contraseña incorrectos.",
            headers={"WWW-Authenticate": "Bearer"}
        )

        if not usuario:
            raise credenciales_invalidas

        if not verify_password(datos.password, usuario.hashed_password):
            raise credenciales_invalidas

        if not usuario.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="El usuario está inactivo."
            )

        return usuario

    @staticmethod
    def generar_token(usuario: User) -> str:
        """Genera un JWT con la identidad y el rol del usuario."""
        return create_access_token(
            data={"sub": str(usuario.id), "email": usuario.email, "role": usuario.role}
        )
