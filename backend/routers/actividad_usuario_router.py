from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter(prefix="/actividad_usuario", tags=["Actividad Usuario"])

class ActividadUsuario(BaseModel):
    UsuarioID: int
    ActividadID: int
    Completada: Optional[bool] = False
    FechaCompletada: Optional[str] = None  # formato YYYY-MM-DD opcional

# 📌 Crear relación usuario-actividad
@router.post("/")
def registrar_actividad_usuario(data: ActividadUsuario):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Verificar que el usuario existe
        cursor.execute("SELECT * FROM usuario WHERE ID=%s", (data.UsuarioID,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Usuario no encontrado")

        # Verificar que la actividad existe
        cursor.execute("SELECT * FROM actividad WHERE ID=%s", (data.ActividadID,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Actividad no encontrada")

        # Insertar registro
        cursor.execute("""
            INSERT INTO actividad_usuario (UsuarioID, ActividadID, Completada, FechaCompletada)
            VALUES (%s, %s, %s, %s)
        """, (data.UsuarioID, data.ActividadID, data.Completada, data.FechaCompletada))
        conn.commit()
        return {"success": True, "message": "Actividad asignada al usuario"}
    finally:
        cursor.close()
        conn.close()

# 📌 Listar actividades de un usuario
@router.get("/usuario/{usuario_id}")
def listar_actividades_usuario(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT au.*, a.Titulo, a.Dificultad, a.Categoria
            FROM actividad_usuario au
            JOIN actividad a ON au.ActividadID = a.ID
            WHERE au.UsuarioID = %s
        """, (usuario_id,))
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

