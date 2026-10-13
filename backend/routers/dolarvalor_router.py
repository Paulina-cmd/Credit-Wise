from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection

router = APIRouter(prefix="/dolar", tags=["Dólar Valor"])

class DolarValor(BaseModel):
    fecha: str
    valorVenta: float
    fechaActualizacion: str
    fuente: str

@router.get("/")
def listar_dolares():
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dolarvalor")
        result = cursor.fetchall()
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.get("/{id}")
def obtener_dolar(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dolarvalor WHERE ID=%s", (id,))
        result = cursor.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail="Valor del dólar no encontrado")
        return {"success": True, "data": result}
    finally:
        cursor.close()
        conn.close()

@router.post("/")
def crear_dolar(dolar: DolarValor):
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO dolarvalor (fecha, valorVenta, fechaActualizacion, fuente)
            VALUES (%s, %s, %s, %s)
        """, (dolar.fecha, dolar.valorVenta, dolar.fechaActualizacion, dolar.fuente))
        conn.commit()
        return {"success": True, "message": "Valor del dólar registrado correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.put("/{id}")
def actualizar_dolar(id: int, dolar: DolarValor):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dolarvalor WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Valor del dólar no encontrado")
        
        cursor.execute("""
            UPDATE dolarvalor
            SET fecha=%s, valorVenta=%s, fechaActualizacion=%s, fuente=%s
            WHERE ID=%s
        """, (dolar.fecha, dolar.valorVenta, dolar.fechaActualizacion, dolar.fuente, id))
        conn.commit()
        return {"success": True, "message": "Valor del dólar actualizado correctamente"}
    finally:
        cursor.close()
        conn.close()

@router.delete("/{id}")
def eliminar_dolar(id: int):
    conn = get_connection()
    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM dolarvalor WHERE ID=%s", (id,))
        if not cursor.fetchone():
            raise HTTPException(status_code=404, detail="Valor del dólar no encontrado")
        
        cursor.execute("DELETE FROM dolarvalor WHERE ID=%s", (id,))
        conn.commit()
        return {"success": True, "message": "Valor del dólar eliminado correctamente"}
    finally:
        cursor.close()
        conn.close()
