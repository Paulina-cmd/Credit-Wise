from pydantic import BaseModel
from typing import Optional

class Usuario(BaseModel):
    ID: Optional[int] = None
    nombre: str
    contrasena: str
    documento: str
    PuntajeCrediticio: Optional[float] = None
    NivelProgreso: Optional[int] = None
    RolID: Optional[int] = None  # 🔹 coincide con FK hacia rolusuario
