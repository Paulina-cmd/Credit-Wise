from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection
from models.historial_model import HistorialMision

router = APIRouter(prefix="/historial", tags=["Historial"])

@router.get("/")
def listar_historial():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT hm.*, m.Titulo as MisionTitulo, m.Dificultad, m.RecompensaPuntos,
                   u.Nombre as UsuarioNombre
            FROM historialmisiones hm
            JOIN mision m ON hm.MisionID = m.ID
            JOIN usuario u ON hm.UsuarioID = u.ID
            ORDER BY hm.FechaCompletado DESC
        """)
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.get("/usuario/{usuario_id}")
def obtener_historial_usuario(usuario_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT hm.*, m.Titulo as MisionTitulo, m.Dificultad, m.RecompensaPuntos,
                   u.Nombre as UsuarioNombre
            FROM historialmisiones hm
            JOIN mision m ON hm.MisionID = m.ID
            JOIN usuario u ON hm.UsuarioID = u.ID
            WHERE hm.UsuarioID = %s
            ORDER BY hm.FechaCompletado DESC
        """, (usuario_id,))
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.post("/")
def registrar_mision_completada(historial: HistorialMision):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado)
            VALUES (%s, %s, %s, %s, NOW())
        """, (historial.UsuarioID, historial.MisionID, historial.PuntosObtenidos, historial.EstadoFinal))
        conn.commit()
        return {"success": True, "message": "Misión registrada en historial correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.post("/completar-mision/{usuario_id}/{mision_id}")
def completar_mision(usuario_id: int, mision_id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        
        # Verificar si la misión existe y obtener sus datos
        cursor.execute("SELECT * FROM mision WHERE ID = %s", (mision_id,))
        mision = cursor.fetchone()
        if not mision:
            raise HTTPException(status_code=404, detail="Misión no encontrada")
        
        # Verificar si el usuario existe
        cursor.execute("SELECT * FROM usuario WHERE ID = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # Registrar en el historial
        cursor.execute("""
            INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado)
            VALUES (%s, %s, %s, %s, NOW())
        """, (usuario_id, mision_id, mision['RecompensaPuntos'], 'completada'))
        
        # Actualizar progreso del usuario (marcar como completada)
        cursor.execute("""
            UPDATE progresousuario 
            SET Estado = 'completada', PorcentajeCompletado = 100 
            WHERE UsuarioID = %s AND MisionID = %s
        """, (usuario_id, mision_id))
        
        # Actualizar puntaje del usuario
        nuevo_puntaje = (usuario['PuntajeCrediticio'] or 0) + mision['RecompensaPuntos']
        cursor.execute("""
            UPDATE usuario 
            SET PuntajeCrediticio = %s 
            WHERE ID = %s
        """, (nuevo_puntaje, usuario_id))
        
        conn.commit()
        
        return {
            "success": True, 
            "message": "Misión completada y registrada en historial",
            "puntos_obtenidos": mision['RecompensaPuntos'],
            "nuevo_puntaje": nuevo_puntaje
        }
        
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def eliminar_historial(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM historialmisiones WHERE ID = %s", (id,))
        conn.commit()
        return {"success": True, "message": "Registro de historial eliminado"}
    finally:
        cursor.close()
        conn.close()

@router.post("/completar-mision/{usuario_id}/{mision_id}")
def completar_mision(usuario_id: int, mision_id: int):
    conn = get_connection()
    cursor = None
    try:
        print(f"🎯 Completando misión: Usuario {usuario_id}, Misión {mision_id}")
        
        cursor = conn.cursor(dictionary=True)
        
        # 1. Verificar si la misión existe
        cursor.execute("SELECT * FROM mision WHERE ID = %s", (mision_id,))
        mision = cursor.fetchone()
        if not mision:
            raise HTTPException(status_code=404, detail="Misión no encontrada")
        
        # 2. Verificar si el usuario existe
        cursor.execute("SELECT * FROM usuario WHERE ID = %s", (usuario_id,))
        usuario = cursor.fetchone()
        if not usuario:
            raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
        # 3. Insertar en historial (VERSIÓN MEJORADA)
        puntos = mision['RecompensaPuntos'] if mision['RecompensaPuntos'] else 50
        cursor.execute("""
            INSERT INTO historialmisiones 
            (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado) 
            VALUES (%s, %s, %s, %s, CURDATE())
        """, (usuario_id, mision_id, puntos, "completada"))
        
        # 4. Actualizar progreso del usuario (si la tabla existe)
        try:
            cursor.execute("""
                UPDATE usuario 
                SET PuntajeCrediticio = COALESCE(PuntajeCrediticio, 0) + %s,
                    NivelProgreso = COALESCE(NivelProgreso, 0) + 5
                WHERE ID = %s
            """, (puntos, usuario_id))
        except Exception as e:
            print(f"⚠️ Error actualizando usuario (no crítico): {str(e)}")
        
        conn.commit()
        
        print(f"✅ Misión {mision_id} completada para usuario {usuario_id}")
        return {
            "success": True, 
            "message": "Misión completada exitosamente",
            "puntos_obtenidos": puntos,
            "mision_id": mision_id,
            "usuario_id": usuario_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Error completando misión: {str(e)}")
        if conn:
            conn.rollback()
        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

