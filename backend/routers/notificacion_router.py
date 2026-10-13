from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection
from typing import Optional

router = APIRouter()

class Notificacion(BaseModel):
    UsuarioID: int
    Mensaje: str

@router.post("/notificacion")
def enviar_notificacion(notif: Notificacion):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO notificacion (UsuarioID, Mensaje) VALUES (%s,%s)",
            (notif.UsuarioID, notif.Mensaje)
        )
        conn.commit()
        return {"message": "Notificación enviada"}
    finally:
        cursor.close()
        conn.close()
