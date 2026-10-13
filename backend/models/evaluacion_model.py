from pydantic import BaseModel
from typing import Optional

class Evaluacion(BaseModel):
    ID: Optional[int] = None
    Tipo: Optional[str] = None
    Resultado: Optional[str] = None
    PuntajeObtenido: Optional[float] = None
    Feedback: Optional[str] = None
    Dificultad: Optional[str] = None
    UsuarioID: Optional[int] = None  # 🔹 FK hacia usuario
    MisionID: Optional[int] = None   # 🔹 FK hacia mision
