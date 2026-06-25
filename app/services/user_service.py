from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import asc
from fastapi import HTTPException, status
from app.models.user_model import User
from app.schemas.user_schema import UserUpdate, UserPatch


class UserService:

    @staticmethod
    def listar_usuarios(
        db: Session,
        role: Optional[str] = None,
        is_active: Optional[bool] = None,
        order_by: Optional[str] = None
    ) -> List[User]:
        """Lista usuarios con filtros opcionales por rol, estado y orden."""
        query = db.query(User)

        if role is not None:
            if role not in ("admin", "support", "user"):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Rol '{role}' no permitido. Usa: admin, support, user."
                )
            query = query.filter(User.role == role.lower())

        if is_active is not None:
            query = query.filter(User.is_active == is_active)

        if order_by == "name":
            query = query.order_by(asc(User.name))
        elif order_by == "created_at":
            query = query.order_by(asc(User.created_at))

        return query.all()

    @staticmethod
    def obtener_por_id(db: Session, user_id: int) -> User:
        """Busca un usuario por ID o lanza 404."""
        usuario = db.query(User).filter(User.id == user_id).first()
        if not usuario:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="El usuario que buscas no existe."
            )
        return usuario

    @staticmethod
    def obtener_por_email(db: Session, email: str) -> Optional[User]:
        """Busca un usuario por email."""
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def verificar_email_duplicado(db: Session, email: str, excluir_id: Optional[int] = None):
        """Lanza 400 si el email ya está en uso por otro usuario."""
        query = db.query(User).filter(User.email == email)
        if excluir_id is not None:
            query = query.filter(User.id != excluir_id)
        if query.first():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ese correo ya existe, intenta con otro."
            )

    @staticmethod
    def actualizar_completo(db: Session, user_id: int, datos: UserUpdate) -> User:
        """Reemplaza todos los campos de un usuario (PUT)."""
        usuario = UserService.obtener_por_id(db, user_id)
        UserService.verificar_email_duplicado(db, datos.email, excluir_id=user_id)
        for campo, valor in datos.model_dump().items():
            setattr(usuario, campo, valor)
        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def actualizar_parcial(db: Session, user_id: int, datos: UserPatch) -> User:
        """Actualiza solo los campos enviados (PATCH)."""
        usuario = UserService.obtener_por_id(db, user_id)
        campos_enviados = datos.model_dump(exclude_unset=True)

        if not campos_enviados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Debes enviar al menos un campo para actualizar."
            )

        if "email" in campos_enviados:
            UserService.verificar_email_duplicado(db, campos_enviados["email"], excluir_id=user_id)

        for campo, valor in campos_enviados.items():
            setattr(usuario, campo, valor)

        db.commit()
        db.refresh(usuario)
        return usuario

    @staticmethod
    def eliminar_usuario(db: Session, user_id: int):
        """Elimina un usuario por ID."""
        usuario = UserService.obtener_por_id(db, user_id)
        db.delete(usuario)
        db.commit()
