"""
MISION CONTROLLER
Maneja toda la lógica de negocio relacionada con misiones
"""
from database import get_connection
from fastapi import HTTPException

class MisionController:
    """Controlador para operaciones de misiones"""
    
    @staticmethod
    def listar_todas():
        """Obtiene todas las misiones disponibles"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID, Titulo, Descripcion, Dificultad, RecompensaPuntos 
                FROM mision 
                ORDER BY Dificultad ASC
            """)
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_id(mision_id: int):
        """Obtiene los detalles de una misión específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID, Titulo, Descripcion, Dificultad, RecompensaPuntos 
                FROM mision 
                WHERE ID = %s
            """, (mision_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Misión no encontrada")
            
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_dificultad(dificultad: str):
        """Obtiene misiones filtradas por dificultad"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT ID, Titulo, Descripcion, Dificultad, RecompensaPuntos 
                FROM mision 
                WHERE Dificultad = %s
                ORDER BY ID ASC
            """, (dificultad,))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear(titulo: str, descripcion: str, dificultad: str, recompensa_puntos: int):
        """Crea una nueva misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO mision (Titulo, Descripcion, Dificultad, RecompensaPuntos)
                VALUES (%s, %s, %s, %s)
            """, (titulo, descripcion, dificultad, recompensa_puntos))
            conn.commit()
            nuevo_id = cursor.lastrowid
            return {"success": True, "message": "Misión creada exitosamente", "mision_id": nuevo_id}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar(mision_id: int, titulo: str = None, descripcion: str = None, 
                   dificultad: str = None, recompensa_puntos: int = None):
        """Actualiza los datos de una misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que la misión existe
            cursor.execute("SELECT * FROM mision WHERE ID = %s", (mision_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Misión no encontrada")

            # Construir query dinámica
            updates = []
            values = []
            if titulo:
                updates.append("Titulo = %s")
                values.append(titulo)
            if descripcion:
                updates.append("Descripcion = %s")
                values.append(descripcion)
            if dificultad:
                updates.append("Dificultad = %s")
                values.append(dificultad)
            if recompensa_puntos is not None:
                updates.append("RecompensaPuntos = %s")
                values.append(recompensa_puntos)

            if updates:
                values.append(mision_id)
                query = f"UPDATE mision SET {', '.join(updates)} WHERE ID = %s"
                cursor.execute(query, values)
                conn.commit()

            return {"success": True, "message": "Misión actualizada exitosamente"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar(mision_id: int):
        """Elimina una misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mision WHERE ID = %s", (mision_id,))
            conn.commit()
            return {"success": True, "message": "Misión eliminada correctamente"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_estadisticas(usuario_id: int = None):
        """Obtiene estadísticas de misiones completadas"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            if usuario_id:
                # Estadísticas de un usuario específico
                cursor.execute("""
                    SELECT 
                        COUNT(hm.ID) as total_completadas,
                        SUM(hm.PuntosObtenidos) as puntos_totales,
                        m.Dificultad,
                        COUNT(CASE WHEN m.Dificultad = 'Fácil' THEN 1 END) as faciles,
                        COUNT(CASE WHEN m.Dificultad = 'Medio' THEN 1 END) as medios,
                        COUNT(CASE WHEN m.Dificultad = 'Difícil' THEN 1 END) as dificiles
                    FROM historialmisiones hm
                    JOIN mision m ON hm.MisionID = m.ID
                    WHERE hm.UsuarioID = %s
                """, (usuario_id,))
            else:
                # Estadísticas globales
                cursor.execute("""
                    SELECT 
                        COUNT(hm.ID) as total_completadas,
                        COUNT(DISTINCT hm.UsuarioID) as usuarios_activos,
                        AVG(hm.PuntosObtenidos) as promedio_puntos
                    FROM historialmisiones hm
                """)
            
            result = cursor.fetchone()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()
