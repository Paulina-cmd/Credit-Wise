"""
EVALUACION CONTROLLER
Maneja toda la lógica de negocio relacionada con evaluaciones
"""
from database import get_connection
from fastapi import HTTPException

class EvaluacionController:
    """Controlador para operaciones de evaluaciones"""
    
    @staticmethod
    def listar_todas():
        """Obtiene todas las evaluaciones disponibles"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    e.ID,
                    e.Tipo,
                    e.Resultado,
                    e.PuntajeObtenido,
                    e.Feedback,
                    e.Dificultad,
                    e.MisionID,
                    m.Titulo as MisionTitulo
                FROM evaluacion e
                LEFT JOIN mision m ON e.MisionID = m.ID
                ORDER BY e.ID DESC
            """)
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_usuario(usuario_id: int):
        """Obtiene todas las evaluaciones de un usuario específico (SOLO LAS SUYAS)"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    e.ID,
                    e.Tipo,
                    e.Resultado,
                    e.PuntajeObtenido,
                    e.Feedback,
                    e.Dificultad,
                    e.MisionID,
                    m.Titulo as MisionTitulo,
                    h.FechaCompletado,
                    h.UsuarioID
                FROM evaluacion e
                LEFT JOIN mision m ON e.MisionID = m.ID
                LEFT JOIN historialmisiones h ON e.MisionID = h.MisionID AND h.UsuarioID = %s
                WHERE h.UsuarioID = %s
                ORDER BY h.FechaCompletado DESC
            """, (usuario_id, usuario_id))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_id(evaluacion_id: int):
        """Obtiene los detalles de una evaluación específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    e.ID,
                    e.Tipo,
                    e.Resultado,
                    e.PuntajeObtenido,
                    e.Feedback,
                    e.Dificultad,
                    e.MisionID,
                    m.Titulo as MisionTitulo
                FROM evaluacion e
                LEFT JOIN mision m ON e.MisionID = m.ID
                WHERE e.ID = %s
            """, (evaluacion_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Evaluación no encontrada")
            
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear(tipo: str, resultado: str, puntaje: float, feedback: str, dificultad: str, mision_id: int):
        """Crea una nueva evaluación"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Verificar que la misión existe
            cursor.execute("SELECT ID FROM mision WHERE ID = %s", (mision_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Misión no encontrada")

            cursor.execute("""
                INSERT INTO evaluacion (Tipo, Resultado, PuntajeObtenido, Feedback, Dificultad, MisionID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tipo, resultado, puntaje, feedback, dificultad, mision_id))
            
            conn.commit()
            nuevo_id = cursor.lastrowid
            return {"success": True, "message": "Evaluación creada", "evaluacion_id": nuevo_id}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def registrar_evaluacion_usuario(usuario_id: int, tipo: str, resultado: str, 
                                     puntaje: float, feedback: str, dificultad: str, mision_id: int):
        """Registra una evaluación completada por un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que el usuario existe
            cursor.execute("SELECT ID FROM usuario WHERE ID = %s", (usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Verificar que la misión existe
            cursor.execute("SELECT RecompensaPuntos FROM mision WHERE ID = %s", (mision_id,))
            mision = cursor.fetchone()
            if not mision:
                raise HTTPException(status_code=404, detail="Misión no encontrada")

            # Crear la evaluación
            cursor.execute("""
                INSERT INTO evaluacion (Tipo, Resultado, PuntajeObtenido, Feedback, Dificultad, MisionID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (tipo, resultado, puntaje, feedback, dificultad, mision_id))
            
            conn.commit()
            
            # Registrar en historial si no existe
            cursor.execute("""
                SELECT ID FROM historialmisiones
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            
            if not cursor.fetchone():
                cursor.execute("""
                    INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado)
                    VALUES (%s, %s, %s, %s, NOW())
                """, (usuario_id, mision_id, puntaje, resultado))
                conn.commit()

            # Actualizar progreso del usuario
            cursor.execute("""
                UPDATE usuario
                SET PuntajeCrediticio = COALESCE(PuntajeCrediticio, 0) + %s,
                    NivelProgreso = COALESCE(NivelProgreso, 0) + %s
                WHERE ID = %s
            """, (puntaje, int(puntaje // 10), usuario_id))
            
            conn.commit()
            
            return {"success": True, "message": "Evaluación registrada exitosamente"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_estadisticas_usuario(usuario_id: int):
        """Obtiene estadísticas de evaluaciones de un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COUNT(e.ID) as total_evaluaciones,
                    AVG(e.PuntajeObtenido) as promedio_puntaje,
                    MAX(e.PuntajeObtenido) as mejor_puntaje,
                    MIN(e.PuntajeObtenido) as peor_puntaje,
                    COUNT(CASE WHEN e.Resultado = 'Aprobado' THEN 1 END) as evaluaciones_aprobadas,
                    COUNT(CASE WHEN e.Resultado = 'Reprobado' THEN 1 END) as evaluaciones_reprobadas
                FROM evaluacion e
                LEFT JOIN historialmisiones h ON e.MisionID = h.MisionID
                WHERE h.UsuarioID = %s
            """, (usuario_id,))
            result = cursor.fetchone()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()
