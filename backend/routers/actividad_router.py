from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter(prefix="/actividades", tags=["Actividades"])

class Actividad(BaseModel):
    Titulo: str
    Contenido: Optional[str] = None
    Categoria: Optional[str] = None
    Dificultad: Optional[str] = None
    MisionID: Optional[int] = None

@router.post("/")
def crear_actividad(actividad: Actividad):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO actividad (Titulo, Contenido, Categoria, Dificultad, MisionID) VALUES (%s,%s,%s,%s,%s)",
            (actividad.Titulo, actividad.Contenido, actividad.Categoria, actividad.Dificultad, actividad.MisionID)
        )
        conn.commit()
        return {"success": True, "message": "Actividad creada"}
    finally:
        cursor.close()
        conn.close()

# Listar todas las actividades
@router.get("/")
def listar_actividades():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM actividad")
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

# Obtener actividades de un usuario con su estado de completado
@router.get("/usuario/{usuario_id}")
def obtener_actividades_usuario(usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Obtener todas las actividades junto con el estado de completado del usuario
        cursor.execute("""
            SELECT 
                a.ID,
                a.Titulo,
                a.Contenido as Descripcion,
                a.Categoria,
                a.Dificultad,
                a.MisionID,
                COALESCE(au.Completada, 0) as Completada,
                au.FechaCompletada
            FROM actividad a
            LEFT JOIN actividad_usuario au ON a.ID = au.ActividadID AND au.UsuarioID = %s
            ORDER BY a.ID
        """, (usuario_id,))
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

# Obtener una actividad específica
@router.get("/{id}")
def obtener_actividad(id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM actividad WHERE ID = %s", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Actividad no encontrada")
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

# Actualizar estado de completado de una actividad para un usuario
@router.put("/{actividad_id}/usuario/{usuario_id}")
def completar_actividad(actividad_id: int, usuario_id: int):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # Verificar si ya existe el registro
        cursor.execute("""
            SELECT * FROM actividad_usuario 
            WHERE ActividadID = %s AND UsuarioID = %s
        """, (actividad_id, usuario_id))
        
        existing = cursor.fetchone()
        
        if existing:
            # Actualizar
            cursor.execute("""
                UPDATE actividad_usuario 
                SET Completada = 1, FechaCompletada = NOW()
                WHERE ActividadID = %s AND UsuarioID = %s
            """, (actividad_id, usuario_id))
        else:
            # Insertar
            cursor.execute("""
                INSERT INTO actividad_usuario (ActividadID, UsuarioID, Completada, FechaCompletada)
                VALUES (%s, %s, 1, NOW())
            """, (actividad_id, usuario_id))
        
        conn.commit()
        return {"success": True, "message": "Actividad marcada como completada"}
    finally:
        cursor.close()
        conn.close()

