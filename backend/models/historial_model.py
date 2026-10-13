from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HistorialMision(BaseModel):
    ID: Optional[int] = None
    UsuarioID: int
    MisionID: int
    PuntosObtenidos: int
    EstadoFinal: str
    FechaCompletado: Optional[str] = None