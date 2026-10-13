from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
from database import get_connection

router = APIRouter(prefix="/evaluaciones", tags=["Evaluaciones"])

class Evaluacion(BaseModel):
    Tipo: str
    Resultado: str
    PuntajeObtenido: float
    Feedback: str
    Dificultad: str
    MisionID: int
    UsuarioID: Optional[int] = None

@router.get("/")
def listar_evaluaciones():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Incluimos datos de historial si existen para que el frontend pueda filtrar por UsuarioID
        cursor.execute("""
            SELECT e.*, m.Titulo AS MisionTitulo, h.UsuarioID AS UsuarioID, h.FechaCompletado AS FechaCreacion
            FROM evaluacion e
            LEFT JOIN mision m ON e.MisionID = m.ID
            LEFT JOIN historialmisiones h ON e.MisionID = h.MisionID
        """)
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.get("/{id}")
def obtener_evaluacion(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, m.Titulo AS MisionTitulo
            FROM evaluacion e
            LEFT JOIN mision m ON e.MisionID = m.ID
            WHERE e.ID=%s
        """, (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.post("/")
def crear_evaluacion(ev: Evaluacion):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Verificar que la misión existe
        cursor.execute("SELECT * FROM mision WHERE ID=%s", (ev.MisionID,))
        mision = cursor.fetchone()
        if not mision:
            raise HTTPException(status_code=404, detail="Misión no encontrada")

        # Insertar evaluación (la tabla puede no contener UsuarioID; intentamos insertar sin esa columna)
        cursor.execute("""
            INSERT INTO evaluacion (Tipo, Resultado, PuntajeObtenido, Feedback, Dificultad, MisionID)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (ev.Tipo, ev.Resultado, ev.PuntajeObtenido, ev.Feedback, ev.Dificultad, ev.MisionID))
        conn.commit()
        inserted_eval_id = cursor.lastrowid

        # Si el frontend envió UsuarioID, registrar en historialmisiones (si no existe)
        nuevo_puntaje = None
        nuevo_nivel = None
        if ev.UsuarioID:
            try:
                cursor.execute("SELECT * FROM historialmisiones WHERE UsuarioID=%s AND MisionID=%s", (ev.UsuarioID, ev.MisionID))
                exists = cursor.fetchone()
                if not exists:
                    cursor.execute("INSERT INTO historialmisiones (UsuarioID, MisionID, PuntosObtenidos, EstadoFinal, FechaCompletado) VALUES (%s,%s,%s,%s,CURDATE())", (ev.UsuarioID, ev.MisionID, ev.PuntajeObtenido, ev.Resultado))
                    conn.commit()

                # Intentar actualizar puntaje y nivel del usuario según puntaje de la evaluación
                try:
                    incremento_nivel = int(ev.PuntajeObtenido // 10) if ev.PuntajeObtenido else 0
                    cursor.execute("""
                        UPDATE usuario
                        SET PuntajeCrediticio = COALESCE(PuntajeCrediticio, 0) + %s,
                            NivelProgreso = COALESCE(NivelProgreso, 0) + %s
                        WHERE ID = %s
                    """, (ev.PuntajeObtenido, incremento_nivel, ev.UsuarioID))
                    conn.commit()
                    # Obtener nuevo estado del usuario
                    cursor.execute("SELECT ID, PuntajeCrediticio, NivelProgreso FROM usuario WHERE ID=%s", (ev.UsuarioID,))
                    usr = cursor.fetchone()
                    if usr:
                        nuevo_puntaje = usr.get('PuntajeCrediticio')
                        nuevo_nivel = usr.get('NivelProgreso')
                except Exception as e:
                    print('Warning: no se pudo actualizar puntaje/nivel del usuario:', str(e))
            except Exception:
                # No consideramos esto crítico; solo logueamos en consola
                print('Warning: no se pudo insertar en historialmisiones (posible ausencia de tabla/columnas)')

        # 🔹 Si la evaluación fue aprobada (por ejemplo, Resultado = "Aprobado")
        if ev.Resultado.lower() == "aprobado":
            # Buscar la actividad asociada a esa misión
            cursor.execute("SELECT * FROM actividad WHERE MisionID=%s", (ev.MisionID,))
            actividad = cursor.fetchone()
            if actividad:
                # Actualizar la relación en actividad_usuario
                cursor.execute("""
                    UPDATE actividad_usuario
                    SET Completada = TRUE, FechaCompletada = CURDATE()
                    WHERE ActividadID = %s
                """, (actividad["ID"],))
                conn.commit()
        return {"success": True, "message": "Evaluación registrada y progreso actualizado", "evaluacion_id": inserted_eval_id, "nuevo_puntaje": nuevo_puntaje, "nuevo_nivel": nuevo_nivel}
    finally:
        cursor.close()
        conn.close()



@router.put("/{id}")
def actualizar_evaluacion(id: int, ev: Evaluacion):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        # Verificar que la evaluación existe
        cursor.execute("SELECT * FROM evaluacion WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")
        
        # Verificar que la misión existe
        cursor.execute("SELECT * FROM mision WHERE ID=%s", (ev.MisionID,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Misión no encontrada")

        cursor.execute("""
            UPDATE evaluacion
            SET Tipo=%s, Resultado=%s, PuntajeObtenido=%s, Feedback=%s, Dificultad=%s, MisionID=%s
            WHERE ID=%s
        """, (ev.Tipo, ev.Resultado, ev.PuntajeObtenido, ev.Feedback, ev.Dificultad, ev.MisionID, id))
        conn.commit()
        return {"success": True, "message": "Evaluación actualizada correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def eliminar_evaluacion(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM evaluacion WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Evaluación no encontrada")
        
        cursor.execute("DELETE FROM evaluacion WHERE ID=%s", (id,))
        conn.commit()
        return {"success": True, "message": "Evaluación eliminada correctamente"}
    finally:
        cursor.close()
        conn.close()


