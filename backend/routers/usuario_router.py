from fastapi import APIRouter, HTTPException
from models.usuario_model import Usuario
from controllers.usuario_controller import UsuarioController
from pydantic import BaseModel

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

# Modelos Pydantic
class UserRegister(BaseModel):
    nombre: str
    contrasena: str
    documento: str
    RolID: int = 2

class UserLogin(BaseModel):
    documento: str
    contrasena: str


# ============ ENDPOINTS DE USUARIOS ============

@router.get("/")
def listar_usuarios():
    """Obtiene todos los usuarios (sin contraseñas)"""
    return UsuarioController.listar_todos()


@router.get("/{id}")
def obtener_usuario(id: int):
    """Obtiene un usuario por su ID"""
    return UsuarioController.obtener_por_id(id)


@router.post("/")
def crear_usuario(usuario: Usuario):
    """Crea un nuevo usuario con contraseña encriptada"""
    return UsuarioController.crear(
        nombre=usuario.nombre,
        contrasena=usuario.contrasena,
        documento=usuario.documento,
        rol_id=usuario.RolID or 2
    )


@router.put("/{id}")
def actualizar_usuario(id: int, usuario: Usuario):
    """Actualiza los datos de un usuario (excepto contraseña)"""
    return UsuarioController.actualizar(
        usuario_id=id,
        nombre=usuario.nombre,
        documento=usuario.documento,
        rol_id=usuario.RolID
    )


@router.delete("/{id}")
def eliminar_usuario(id: int):
    """Elimina un usuario"""
    return UsuarioController.eliminar(id)


# ============ ENDPOINTS DE AUTENTICACION ============

@router.post("/register")
def register(user: UserRegister):
    """Registra un nuevo usuario"""
    try:
        return UsuarioController.crear(
            nombre=user.nombre,
            contrasena=user.contrasena,
            documento=user.documento,
            rol_id=user.RolID
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(user: UserLogin):
    """Autentica un usuario y retorna sus datos"""
    return UsuarioController.autenticar(
        documento=user.documento,
        contrasena=user.contrasena
    )


# ============ ENDPOINTS DE PROGRESO ============

@router.put("/{usuario_id}/progreso")
def actualizar_progreso_usuario(usuario_id: int, puntaje: int = 0, nivel: int = 0):
    """Actualiza el puntaje crediticio y nivel de un usuario"""
    return UsuarioController.actualizar_progreso(
        usuario_id=usuario_id,
        puntaje_adicional=puntaje,
        nivel_adicional=nivel
    )


