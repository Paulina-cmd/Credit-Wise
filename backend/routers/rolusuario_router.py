from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection

router = APIRouter(prefix="/roles", tags=["Roles de Usuario"])

class RolUsuario(BaseModel):
    Nombre: str

@router.get("/")
def listar_roles():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rolusuario")
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.get("/{id}")
def obtener_rol(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rolusuario WHERE ID=%s", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.post("/")
def crear_rol(rol: RolUsuario):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO rolusuario (Nombre) VALUES (%s)", (rol.Nombre,))
        conn.commit()
        return {"success": True, "message": "Rol creado correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.put("/{id}")
def actualizar_rol(id: int, rol: RolUsuario):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rolusuario WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        cursor.execute("UPDATE rolusuario SET Nombre=%s WHERE ID=%s", (rol.Nombre, id))
        conn.commit()
        return {"success": True, "message": "Rol actualizado correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def eliminar_rol(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM rolusuario WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Rol no encontrado")
        
        cursor.execute("DELETE FROM rolusuario WHERE ID=%s", (id,))
        conn.commit()
        return {"success": True, "message": "Rol eliminado correctamente"}
    finally:
        cursor.close()
        conn.close()
