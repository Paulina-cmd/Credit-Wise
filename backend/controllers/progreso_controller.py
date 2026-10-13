"""
PROGRESO CONTROLLER
Maneja toda la lógica de negocio relacionada con el progreso del usuario en misiones
"""
from database import get_connection
from fastapi import HTTPException

class ProgresoController:
    """Controlador para operaciones de progreso de usuario"""
    
    @staticmethod
    def obtener_progreso_usuario(usuario_id: int):
        """Obtiene el progreso actual de un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    pu.ID,
                    pu.UsuarioID,
                    pu.MisionID,
                    pu.Estado,
                    pu.PorcentajeCompletado,
                    m.Titulo as MisionTitulo,
                    m.Dificultad,
                    u.Nombre as UsuarioNombre
                FROM progresousuario pu
                JOIN usuario u ON pu.UsuarioID = u.ID
                JOIN mision m ON pu.MisionID = m.ID
                WHERE pu.UsuarioID = %s
                ORDER BY pu.MisionID ASC
            """, (usuario_id,))
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_progreso_mision(usuario_id: int, mision_id: int):
        """Obtiene el progreso de un usuario en una misión específica"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT 
                    ID,
                    UsuarioID,
                    MisionID,
                    Estado,
                    PorcentajeCompletado
                FROM progresousuario
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            result = cursor.fetchone()
            
            if not result:
                return {"success": True, "data": None}
            
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear_progreso(usuario_id: int, mision_id: int, estado: str = "iniciado", porcentaje: float = 0.0):
        """Crea un registro de progreso para un usuario en una misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            # Verificar que no existe un progreso previo
            cursor.execute("""
                SELECT ID FROM progresousuario
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Ya existe un progreso para esta misión")

            cursor.execute("""
                INSERT INTO progresousuario (UsuarioID, MisionID, Estado, PorcentajeCompletado)
                VALUES (%s, %s, %s, %s)
            """, (usuario_id, mision_id, estado, porcentaje))
            
            conn.commit()
            nuevo_id = cursor.lastrowid
            return {"success": True, "message": "Progreso creado", "progreso_id": nuevo_id}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar_progreso(usuario_id: int, mision_id: int, porcentaje: float = None, estado: str = None):
        """Actualiza el progreso de un usuario en una misión"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que el progreso existe
            cursor.execute("""
                SELECT ID FROM progresousuario
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Progreso no encontrado")

            # Construir query dinámica
            updates = []
            values = []
            
            if porcentaje is not None:
                updates.append("PorcentajeCompletado = %s")
                values.append(porcentaje)
            
            if estado:
                updates.append("Estado = %s")
                values.append(estado)

            if updates:
                values.extend([usuario_id, mision_id])
                query = f"UPDATE progresousuario SET {', '.join(updates)} WHERE UsuarioID = %s AND MisionID = %s"
                cursor.execute(query, values)
                conn.commit()

            return {"success": True, "message": "Progreso actualizado"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def completar_mision(usuario_id: int, mision_id: int):
        """Marca una misión como completada (100%)"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE progresousuario
                SET Estado = 'completado', PorcentajeCompletado = 100.0
                WHERE UsuarioID = %s AND MisionID = %s
            """, (usuario_id, mision_id))
            
            conn.commit()
            return {"success": True, "message": "Misión marcada como completada"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_resumen_progreso(usuario_id: int):
        """Obtiene un resumen del progreso general del usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Obtener estadísticas de progreso
            cursor.execute("""
                SELECT 
                    COUNT(ID) as total_misiones,
                    SUM(CASE WHEN Estado = 'completado' THEN 1 ELSE 0 END) as misiones_completadas,
                    SUM(CASE WHEN Estado = 'iniciado' THEN 1 ELSE 0 END) as misiones_iniciadas,
                    AVG(PorcentajeCompletado) as progreso_promedio
                FROM progresousuario
                WHERE UsuarioID = %s
            """, (usuario_id,))
            
            resultado = cursor.fetchone()
            
            # También obtener datos del usuario
            cursor.execute("""
                SELECT PuntajeCrediticio, NivelProgreso
                FROM usuario
                WHERE ID = %s
            """, (usuario_id,))
            
            usuario = cursor.fetchone()
            
            return {
                "success": True,
                "data": {
                    "progreso_misiones": resultado,
                    "usuario": usuario
                }
            }
        finally:
            cursor.close()
            conn.close()
