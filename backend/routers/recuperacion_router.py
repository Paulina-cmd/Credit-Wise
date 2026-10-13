from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import get_connection  # usa el mismo de tus otros endpoints

router = APIRouter(prefix="/recuperacion", tags=["Recuperación de contraseña"])

class PasswordReset(BaseModel):
    documento: str
    nueva_contrasena: str

@router.put("/restablecer")
def restablecer_contrasena(datos: PasswordReset):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuario WHERE Documento = %s", (datos.documento,))
    usuario = cursor.fetchone()

    if not usuario:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    cursor.execute(
        "UPDATE usuario SET Contrasena = %s WHERE Documento = %s",
        (datos.nueva_contrasena, datos.documento)
    )
    conn.commit()
    conn.close()

    return {"mensaje": "✅ Contraseña actualizada correctamente"}
