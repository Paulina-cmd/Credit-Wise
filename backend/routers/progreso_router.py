from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter()

class ProgresoUsuario(BaseModel):
    Estado: Optional[str] = None
    PorcentajeCompletado: Optional[float] = None
    UsuarioID: int
    MisionID: int

@router.post("/progreso")
def crear_progreso(progreso: ProgresoUsuario):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO progresousuario (Estado, PorcentajeCompletado, UsuarioID, MisionID) VALUES (%s,%s,%s,%s)",
            (progreso.Estado, progreso.PorcentajeCompletado, progreso.UsuarioID, progreso.MisionID)
        )
        conn.commit()
        return {"message": "Progreso registrado"}
    finally:
        cursor.close()
        conn.close()
