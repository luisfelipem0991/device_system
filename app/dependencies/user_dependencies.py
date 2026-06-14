from fastapi import HTTPException, status
from app.data.users_db import db_users

# Dependencia para buscar un usuario por ID o disparar un 404 automáticamente
def get_user_or_404(user_id: int) -> dict:
    for usuario in db_users:
        if usuario["id"] == user_id:
            return usuario
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail="El usuario que buscas no existe."
    )

# Dependencia para verificar si un correo está repetido
# Añadimos "excluir_id" para que al editar un usuario, no se estalle consigo mismo si deja su mismo correo
def verificar_correo_duplicado(email: str, excluir_id: int = None):
    for usuario in db_users:
        if usuario["email"] == email and usuario["id"] != excluir_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Ese correo ya existe, intenta con otro."
            )