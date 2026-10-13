"""
USUARIO CONTROLLER
Maneja toda la lógica de negocio relacionada con usuarios
"""
from database import get_connection
from fastapi import HTTPException
import bcrypt

class UsuarioController:
    """Controlador para operaciones de usuarios"""
    
    @staticmethod
    def listar_todos():
        """Obtiene todos los usuarios"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT ID, Nombre, Documento, PuntajeCrediticio, NivelProgreso, RolID FROM usuario")
            result = cursor.fetchall()
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def obtener_por_id(usuario_id: int):
        """Obtiene un usuario por su ID"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT ID, Nombre, Documento, PuntajeCrediticio, NivelProgreso, RolID FROM usuario WHERE ID = %s", (usuario_id,))
            result = cursor.fetchone()
            if not result:
                raise HTTPException(status_code=404, detail="Usuario no encontrado")
            return {"success": True, "data": result}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def crear(nombre: str, contrasena: str, documento: str, rol_id: int = 2):
        """Crea un nuevo usuario con contraseña encriptada"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar si el documento ya existe
            cursor.execute("SELECT * FROM usuario WHERE Documento = %s", (documento,))
            if cursor.fetchone():
                raise HTTPException(status_code=400, detail="Documento ya registrado")

            # Encriptar contraseña
            hashed = bcrypt.hashpw(contrasena.encode('utf-8'), bcrypt.gensalt())

            # Crear usuario
            cursor.execute("""
                INSERT INTO usuario (Nombre, Contrasena, Documento, PuntajeCrediticio, NivelProgreso, RolID)
                VALUES (%s, %s, %s, 0, 0, %s)
            """, (nombre, hashed.decode('utf-8'), documento, rol_id))
            
            conn.commit()
            nuevo_id = cursor.lastrowid
            return {"success": True, "message": "Usuario creado exitosamente", "usuario_id": nuevo_id}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def autenticar(documento: str, contrasena: str):
        """Autentica un usuario y retorna sus datos"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Buscar usuario por documento
            cursor.execute("""
                SELECT ID, Nombre, Documento, Contrasena, PuntajeCrediticio, NivelProgreso, RolID 
                FROM usuario WHERE Documento = %s
            """, (documento,))
            usuario = cursor.fetchone()

            if not usuario:
                raise HTTPException(status_code=401, detail="Usuario no encontrado")

            # Verificar contraseña
            if not bcrypt.checkpw(contrasena.encode('utf-8'), usuario['Contrasena'].encode('utf-8')):
                raise HTTPException(status_code=401, detail="Contraseña incorrecta")

            # Retornar datos del usuario (sin la contraseña)
            return {
                "success": True, 
                "usuario": {
                    "ID": usuario['ID'],
                    "Nombre": usuario['Nombre'],
                    "Documento": usuario['Documento'],
                    "PuntajeCrediticio": usuario['PuntajeCrediticio'],
                    "NivelProgreso": usuario['NivelProgreso'],
                    "RolID": usuario['RolID']
                }
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar(usuario_id: int, nombre: str = None, documento: str = None, rol_id: int = None):
        """Actualiza los datos de un usuario"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Verificar que el usuario existe
            cursor.execute("SELECT * FROM usuario WHERE ID = %s", (usuario_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Usuario no encontrado")

            # Si intenta cambiar documento, verificar que no esté en uso
            if documento:
                cursor.execute("SELECT * FROM usuario WHERE Documento = %s AND ID != %s", (documento, usuario_id))
                if cursor.fetchone():
                    raise HTTPException(status_code=400, detail="Documento ya registrado por otro usuario")

            # Construir query dinámica
            updates = []
            values = []
            if nombre:
                updates.append("Nombre = %s")
                values.append(nombre)
            if documento:
                updates.append("Documento = %s")
                values.append(documento)
            if rol_id is not None:
                updates.append("RolID = %s")
                values.append(rol_id)

            if updates:
                values.append(usuario_id)
                query = f"UPDATE usuario SET {', '.join(updates)} WHERE ID = %s"
                cursor.execute(query, values)
                conn.commit()

            return {"success": True, "message": "Usuario actualizado exitosamente"}
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def actualizar_progreso(usuario_id: int, puntaje_adicional: int = 0, nivel_adicional: int = 0):
        """Actualiza el puntaje crediticio y nivel de progreso"""
        conn = get_connection()
        try:
            cursor = conn.cursor(dictionary=True)
            
            # Actualizar puntaje y nivel
            cursor.execute("""
                UPDATE usuario
                SET PuntajeCrediticio = COALESCE(PuntajeCrediticio, 0) + %s,
                    NivelProgreso = COALESCE(NivelProgreso, 0) + %s
                WHERE ID = %s
            """, (puntaje_adicional, nivel_adicional, usuario_id))
            
            conn.commit()
            
            # Obtener nuevos valores
            cursor.execute("SELECT PuntajeCrediticio, NivelProgreso FROM usuario WHERE ID = %s", (usuario_id,))
            resultado = cursor.fetchone()
            
            return {
                "success": True, 
                "message": "Progreso actualizado",
                "PuntajeCrediticio": resultado['PuntajeCrediticio'],
                "NivelProgreso": resultado['NivelProgreso']
            }
        finally:
            cursor.close()
            conn.close()

    @staticmethod
    def eliminar(usuario_id: int):
        """Elimina un usuario de la base de datos"""
        conn = get_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM usuario WHERE ID = %s", (usuario_id,))
            conn.commit()
            return {"success": True, "message": "Usuario eliminado correctamente"}
        finally:
            cursor.close()
            conn.close()
