from typing import List, Optional
from app.data.users_db import db_users
from app.schemas.user_schema import UserCreate, UserUpdatePartial
from fastapi import HTTPException, status

class UserService:
    
    @staticmethod
    def listar_usuarios(role: Optional[str] = None, is_active: Optional[bool] = None) -> List[dict]:
        resultado = db_users
        if role is not None:
            resultado = [u for u in resultado if u["role"] == role.lower()]
        if is_active is not None:
            resultado = [u for u in resultado if u["is_active"] == is_active]
        return resultado

    @staticmethod
    def crear_usuario(user_in: UserCreate) -> dict:
        nuevo_id = db_users[-1]["id"] + 1 if db_users else 1
        nuevo_usuario = {"id": nuevo_id, **user_in.model_dump()}
        db_users.append(nuevo_usuario)
        return nuevo_usuario

    @staticmethod
    def actualizar_completo(usuario_actual: dict, datos_nuevos: UserCreate) -> dict:
        # Reemplaza absolutamente todos los campos del usuario (PUT)
        usuario_actual.update(datos_nuevos.model_dump())
        return usuario_actual

    @staticmethod
    def actualizar_parcial(usuario_actual: dict, datos_nuevos: UserUpdatePartial) -> dict:
        # Extraemos solo las llaves que el usuario mandó en el JSON, ignorando los None
        campos_enviados = datos_nuevos.model_dump(exclude_unset=True)
        
        # Validación Fase 6: Si el cuerpo del PATCH viene completamente vacío soltamos error 400
        if not campos_enviados:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Intento de actualización sin datos. Debe enviar al menos un campo."
            )
            
        usuario_actual.update(campos_enviados)
        return usuario_actual

    @staticmethod
    def eliminar_usuario(usuario_actual: dict):
        db_users.remove(usuario_actual)