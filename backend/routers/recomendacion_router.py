from fastapi import APIRouter
from database import get_connection

router = APIRouter()


@router.get("/recomendaciones")
def listar_recomendaciones():
    """Intenta leer la tabla `recomendaciones`. Si falla, devuelve una lista por defecto."""
    try:
        conn = get_connection()
        cursor = conn.cursor(dictionary=True)
        # Ajusta los nombres de columnas si tu tabla usa otros nombres
        cursor.execute("SELECT ID, Titulo, Descripcion, DescripcionDetallada FROM recomendaciones")
        rows = cursor.fetchall()
        cursor.close()
        conn.close()

        # Asegurar que devolvemos un array
        if not rows:
            return {"success": True, "data": []}
        return {"success": True, "data": rows}
    except Exception:
        # En caso de que la tabla no exista o falle la consulta, devolvemos recomendaciones por defecto
        defaults = [
            {
                "ID": 1,
                "Titulo": "💰 Crea un fondo de emergencia",
                "Descripcion": "Reserva al menos 3 meses de gastos básicos.",
                "DescripcionDetallada": "Un fondo de emergencia te protege ante imprevistos como pérdida de empleo, gastos médicos o reparaciones urgentes. Calcula tus gastos mensuales esenciales y multiplica por 3."
            },
            {
                "ID": 2,
                "Titulo": "💳 Usa máximo el 30% de tu crédito",
                "Descripcion": "Protege tu puntaje crediticio.",
                "DescripcionDetallada": "Mantener tu utilización de crédito por debajo del 30% demuestra manejo responsable y mejora tu score crediticio. Revisa tus límites y ajusta tu gasto mensual."
            }
        ]
        return {"success": True, "data": defaults}
