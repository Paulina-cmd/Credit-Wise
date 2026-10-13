"""
HISTORIAL CONTROLLER
Maneja toda la lógica de negocio relacionada con el historial de misiones completadas
"""
from database import get_connection
from fastapi import HTTPException
from datetime import datetime

class HistorialController:
    """Controlador para operaciones de historial de misiones"""
    
    @staticmethod
    def listar_todo():
        """Obtiene el historial completo (todas las misiones completadas por todos los usuarios)"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    hm.ID,
                    hm.UsuarioID,
                    hm.MisionID,
                    hm.PuntosObtenidos,
                    hm.EstadoFinal,
                    hm.FechaCompletado,
                    m.Titulo as MisionTitulo,
                    m.Dificultad,
                    m.RecompensaPuntos,
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

    @staticmethod
    def obtener_por_usuario(usuario_id: int):
        """Obtiene el historial de un usuario específico (SOLO SUS MISIONES)"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    hm.ID,
                    hm.UsuarioID,
                    hm.MisionID,
                    hm.PuntosObtenidos,
                    hm.EstadoFinal,
                    hm.FechaCompletado,
                    m.Titulo as MisionTitulo,
                    m.Dificultad,
                    m.RecompensaPuntos,
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

    @staticmethod
    def obtener_por_mision(mision_id: int):
        """Obtiene el historial de una misión específica (quién la completó)"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    hm.ID,
                    hm.UsuarioID,
                    hm.MisionID,
                    hm.PuntosObtenidos,
                    hm.EstadoFinal,
                    hm.FechaCompletado,
                    u.Nombre as UsuarioNombre,
                    u.Documento
                FROM historialmisiones hm
                JOIN usuario u ON hm.UsuarioID = u.ID
                WHERE hm.MisionID = %s
                ORDER BY hm.FechaCompletado DESC
            """, (mision_id,))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def registrar_mision_completada(usuario_id: int, mision_id: int, puntos_obtenidos: int, estado_final: str):
        """Registra que un usuario completó una misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que el usuario existe
            cursor.execute("SELECT ID FROM usuario WHERE ID = %s", (usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Verificar que la misión existe
            cursor.execute("SELECT ID, RecompensaPuntos FROM mision WHERE ID = %s", (mision_id,))
            mision = cursor.fetchone()
            if not mision:
                raise HTTPException(status_code=404, detail="Misión no encontrada")

            # Verificar si ya fue completada
            cursor.execute("""
                SELECT ID FROM historialmisiones 
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Esta misión ya fue completada por este usuario")

            # Registrar la misión completada
            cursor.execute("""
                INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado)
                VALUES (%s, %s, %s, %s, NOW())
            """, (usuario_id, mision_id, puntos_obtenidos, estado_final))
            
            conn.commit()
            
            # Actualizar el progreso del usuario
            cursor.execute("""
                UPDATE usuario
                SET PuntajeCrediticio = COALESCE(PuntajeCrediticio, 0) + %s,
                    NivelProgreso = COALESCE(NivelProgreso, 0) + %s
                WHERE ID = %s
            """, (puntos_obtenidos, puntos_obtenidos // 10, usuario_id))
            
            conn.commit()
            
            return {"success": True, "message": "Misión registrada como completada"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_estadisticas_usuario(usuario_id: int):
        """Obtiene estadísticas del historial de un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COUNT(hm.ID) as total_misiones,
                    SUM(hm.PuntosObtenidos) as puntos_totales,
                    AVG(hm.PuntosObtenidos) as promedio_puntos,
                    MAX(hm.FechaCompletado) as ultima_mision,
                    COUNT(CASE WHEN m.Dificultad = 'Fácil' THEN 1 END) as misiones_faciles,
                    COUNT(CASE WHEN m.Dificultad = 'Medio' THEN 1 END) as misiones_medias,
                    COUNT(CASE WHEN m.Dificultad = 'Difícil' THEN 1 END) as misiones_dificiles
                FROM historialmisiones hm
                JOIN mision m ON hm.MisionID = m.ID
                WHERE hm.UsuarioID = %s
            """, (usuario_id,))
            result = cursor.fetchone()
            
            if not result:
                return {
                    "success": True,
                    "data": {
                        "total_misiones": 0,
                        "puntos_totales": 0,
                        "promedio_puntos": 0,
                        "misiones_faciles": 0,
                        "misiones_medias": 0,
                        "misiones_dificiles": 0
                    }
                }
            
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()
