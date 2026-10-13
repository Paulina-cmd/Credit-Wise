"""
ACTIVIDAD CONTROLLER
Maneja toda la lógica de negocio relacionada con actividades
"""
from database import get_connection
from fastapi import HTTPException

class ActividadController:
    """Controlador para operaciones de actividades"""
    
    @staticmethod
    def listar_todas():
        """Obtiene todas las actividades disponibles"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    a.ID,
                    a.Titulo,
                    a.Contenido,
                    a.Categoria,
                    a.Dificultad,
                    a.UsuarioID,
                    a.MisionID,
                    m.Titulo as MisionTitulo
                FROM actividad a
                LEFT JOIN mision m ON a.MisionID = m.ID
                ORDER BY a.ID DESC
            """)
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_usuario(usuario_id: int):
        """Obtiene todas las actividades de un usuario específico (SOLO LAS SUYAS)"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    a.ID,
                    a.Titulo,
                    a.Contenido,
                    a.Categoria,
                    a.Dificultad,
                    a.MisionID,
                    m.Titulo as MisionTitulo,
                    COALESCE(au.Completada, 0) as Completada,
                    au.FechaCompletada
                FROM actividad a
                LEFT JOIN mision m ON a.MisionID = m.ID
                LEFT JOIN actividad_usuario au ON a.ID = au.ActividadID AND au.UsuarioID = %s
                WHERE a.UsuarioID = %s OR a.UsuarioID IS NULL
                ORDER BY a.ID ASC
            """, (usuario_id, usuario_id))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_mision(mision_id: int):
        """Obtiene todas las actividades de una misión específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    a.ID,
                    a.Titulo,
                    a.Contenido,
                    a.Categoria,
                    a.Dificultad,
                    a.MisionID
                FROM actividad a
                WHERE a.MisionID = %s
                ORDER BY a.ID ASC
            """, (mision_id,))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_id(actividad_id: int):
        """Obtiene los detalles de una actividad específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    a.ID,
                    a.Titulo,
                    a.Contenido,
                    a.Categoria,
                    a.Dificultad,
                    a.UsuarioID,
                    a.MisionID,
                    m.Titulo as MisionTitulo
                FROM actividad a
                LEFT JOIN mision m ON a.MisionID = m.ID
                WHERE a.ID = %s
            """, (actividad_id,))
            result = cursor.fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="Actividad no encontrada")
            
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear(titulo: str, contenido: str, categoria: str, dificultad: str, 
              mision_id: int = None, usuario_id: int = None):
        """Crea una nueva actividad"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Si se especifica una misión, verificar que existe
            if mision_id:
                cursor.execute("SELECT ID FROM mision WHERE ID = %s", (mision_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="Misión no encontrada")

            # Si se especifica un usuario, verificar que existe
            if usuario_id:
                cursor.execute("SELECT ID FROM usuario WHERE ID = %s", (usuario_id,))
                if not cursor.fetchone():
                    raise HTTPException(status_code=404, detail="Usuario no encontrado")

            cursor.execute("""
                INSERT INTO actividad (Titulo, Contenido, Categoria, Dificultad, MisionID, UsuarioID)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (titulo, contenido, categoria, dificultad, mision_id, usuario_id))
            
            conn.commit()
            nuevo_id = cursor.lastrowid
            return {"success": True, "message": "Actividad creada", "actividad_id": nuevo_id}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def completar_actividad(usuario_id: int, actividad_id: int):
        """Marca una actividad como completada por un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que la actividad existe
            cursor.execute("SELECT ID FROM actividad WHERE ID = %s", (actividad_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Actividad no encontrada")

            # Verificar que el usuario existe
            cursor.execute("SELECT ID FROM usuario WHERE ID = %s", (usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Verificar si ya existe el registro
            cursor.execute("""
                SELECT ID FROM actividad_usuario 
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
                # Insertar nuevo registro
                cursor.execute("""
                    INSERT INTO actividad_usuario (ActividadID, UsuarioID, Completada, FechaCompletada)
                    VALUES (%s, %s, 1, NOW())
                """, (actividad_id, usuario_id))
            
            conn.commit()
            return {"success": True, "message": "Actividad marcada como completada"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_estadisticas_usuario(usuario_id: int):
        """Obtiene estadísticas de actividades completadas por un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    COUNT(DISTINCT a.ID) as total_actividades,
                    COUNT(DISTINCT CASE WHEN au.Completada = 1 THEN a.ID END) as actividades_completadas,
                    COUNT(DISTINCT a.Categoria) as categorias_trabajadas
                FROM actividad a
                LEFT JOIN actividad_usuario au ON a.ID = au.ActividadID AND au.UsuarioID = %s
                WHERE a.UsuarioID = %s OR a.UsuarioID IS NULL
            """, (usuario_id, usuario_id))
            result = cursor.fetchone()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()
