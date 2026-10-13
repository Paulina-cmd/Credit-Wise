from pydantic import BaseModel
from typing import Optional

class ProgresoUsuario(BaseModel):
    ID: Optional[int] = None
    Estado: Optional[str] = None
    PorcentajeCompletado: Optional[float] = None
    UsuarioID: Optional[int] = None  # 🔹 FK hacia usuario
    MisionID: Optional[int] = None   # 🔹 FK hacia mision
