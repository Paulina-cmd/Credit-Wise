from pydantic import BaseModel
from typing import Optional

class DolarValor(BaseModel):
    ID: Optional[int] = None
    fecha: Optional[str] = None
    valorVenta: Optional[float] = None
    fechaActualizacion: Optional[str] = None
    fuente: Optional[str] = None
