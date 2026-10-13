from pydantic import BaseModel

class RolUsuario(BaseModel):
    ID: int
    Nombre: str
