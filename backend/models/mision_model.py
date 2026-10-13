from pydantic import BaseModel
from typing import Optional

class Mision(BaseModel):
    ID: Optional[int] = None
    Titulo: str
    Descripcion: Optional[str] = None
    Dificultad: Optional[str] = None
    RecompensaPuntos: Optional[int] = None
    Documento: Optional[str] = None
