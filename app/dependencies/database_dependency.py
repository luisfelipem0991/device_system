from app.database.connection import get_db
from sqlalchemy.orm import Session
from fastapi import Depends

# Re-exportamos get_db como dependencia lista para usar con Depends()
def get_database(db: Session = Depends(get_db)) -> Session:
    """Dependencia que entrega una sesión activa de base de datos."""
    return db
