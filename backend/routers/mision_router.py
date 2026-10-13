from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter()

class Mision(BaseModel):
    Titulo: str
    Descripcion: Optional[str] = None
    Dificultad: Optional[str] = None
    RecompensaPuntos: Optional[int] = None
    Documento: Optional[str] = None

@router.post("/mision")
def crear_mision(mision: Mision):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO mision (Titulo, Descripcion, Dificultad, RecompensaPuntos, Documento) VALUES (%s,%s,%s,%s,%s)",
            (mision.Titulo, mision.Descripcion, mision.Dificultad, mision.RecompensaPuntos, mision.Documento)
        )
        conn.commit()
        return {"message": "Misión creada"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    finally:
        cursor.close()
        conn.close()

@router.get("/misiones")
def listar_misiones():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM mision")
        misiones = cursor.fetchall()
        return misiones
    finally:
        cursor.close()
        conn.close()




