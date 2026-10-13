# 📚 Documentación de la Arquitectura de Controladores

## Estructura del Proyecto Backend

```
backend/
├── controllers/          # 🔧 Lógica de negocio (nueva carpeta)
│   ├── __init__.py
│   ├── usuario_controller.py      # Operaciones de usuarios
│   ├── mision_controller.py        # Operaciones de misiones
│   ├── historial_controller.py     # Historial de misiones completadas
│   ├── progreso_controller.py      # Progreso del usuario en misiones
│   ├── evaluacion_controller.py    # Evaluaciones de usuarios
│   └── actividad_controller.py     # Actividades por misión
├── routers/              # 🛣️ Endpoints/Rutas de la API
│   ├── usuario_router.py
│   ├── mision_router.py
│   ├── historial_router.py
│   └── ...
├── models/               # 📦 Esquemas Pydantic (validación de datos)
│   ├── usuario_model.py
│   ├── mision_model.py
│   └── ...
├── database.py           # 🗄️ Conexión a base de datos
└── main.py               # 🚀 Aplicación FastAPI principal
```

---

## ¿Qué es un Controlador?

Un **controlador** es una clase que concentra toda la lógica de negocio relacionada con una entidad. Separa la lógica de los endpoints, haciendo el código más limpio, reutilizable y fácil de mantener.

### Ventajas:

✅ **Separación de responsabilidades** - Routers solo definen endpoints, controllers manejan lógica
✅ **Reutilización de código** - La misma lógica se puede usar desde múltiples routers
✅ **Fácil de probar** - Puedes testear la lógica sin necesidad de crear requests HTTP
✅ **Mantenibilidad** - Los cambios en lógica se hacen en un solo lugar

---

## Controladores Disponibles

### 1. **UsuarioController**
Maneja todas las operaciones relacionadas con usuarios.

**Métodos principales:**
- `listar_todos()` - Obtiene todos los usuarios
- `obtener_por_id(usuario_id)` - Obtiene un usuario específico
- `crear(nombre, contrasena, documento, rol_id)` - Crea un nuevo usuario
- `autenticar(documento, contrasena)` - Autentica un usuario (login)
- `actualizar(usuario_id, nombre, documento, rol_id)` - Actualiza datos
- `actualizar_progreso(usuario_id, puntaje_adicional, nivel_adicional)` - Actualiza puntaje y nivel
- `eliminar(usuario_id)` - Elimina un usuario

**Ejemplo de uso en router:**
```python
@router.post("/login")
def login(user: UserLogin):
    return UsuarioController.autenticar(user.documento, user.contrasena)
```

---

### 2. **MisionController**
Maneja todas las operaciones relacionadas con misiones.

**Métodos principales:**
- `listar_todas()` - Obtiene todas las misiones
- `obtener_por_id(mision_id)` - Obtiene una misión específica
- `obtener_por_dificultad(dificultad)` - Filtra por dificultad
- `crear(titulo, descripcion, dificultad, recompensa_puntos)` - Crea misión
- `actualizar(mision_id, ...)` - Actualiza una misión
- `obtener_estadisticas(usuario_id)` - Estadísticas de misiones completadas
- `eliminar(mision_id)` - Elimina una misión

---

### 3. **HistorialController**
Maneja el historial de misiones completadas por usuarios.

**Métodos principales:**
- `listar_todo()` - Obtiene historial completo
- `obtener_por_usuario(usuario_id)` - **SOLO el historial de ese usuario** ⭐
- `obtener_por_mision(mision_id)` - Quién completó esta misión
- `registrar_mision_completada(usuario_id, mision_id, puntos, estado)` - Registra completado
- `obtener_estadisticas_usuario(usuario_id)` - Stats del usuario

**Importante:** El método `obtener_por_usuario()` filtra automáticamente por el usuario, asegurando que solo ve su propio historial.

---

### 4. **ProgresoController**
Maneja el progreso del usuario en cada misión.

**Métodos principales:**
- `obtener_progreso_usuario(usuario_id)` - Progreso en todas las misiones
- `obtener_progreso_mision(usuario_id, mision_id)` - Progreso en misión específica
- `crear_progreso(usuario_id, mision_id, estado, porcentaje)` - Crea un registro
- `actualizar_progreso(usuario_id, mision_id, porcentaje, estado)` - Actualiza progreso
- `completar_mision(usuario_id, mision_id)` - Marca como completada (100%)
- `obtener_resumen_progreso(usuario_id)` - Resumen general

---

### 5. **EvaluacionController**
Maneja las evaluaciones de usuarios en misiones.

**Métodos principales:**
- `listar_todas()` - Todas las evaluaciones
- `obtener_por_usuario(usuario_id)` - **SOLO las evaluaciones de ese usuario** ⭐
- `obtener_por_id(evaluacion_id)` - Evaluación específica
- `crear(tipo, resultado, puntaje, feedback, dificultad, mision_id)` - Crea evaluación
- `registrar_evaluacion_usuario(usuario_id, ...)` - Registra evaluación completada
- `obtener_estadisticas_usuario(usuario_id)` - Stats de evaluaciones

---

### 6. **ActividadController**
Maneja las actividades dentro de misiones.

**Métodos principales:**
- `listar_todas()` - Todas las actividades
- `obtener_por_usuario(usuario_id)` - **SOLO las actividades de ese usuario** ⭐
- `obtener_por_mision(mision_id)` - Actividades de una misión
- `obtener_por_id(actividad_id)` - Actividad específica
- `crear(titulo, contenido, categoria, dificultad, mision_id, usuario_id)` - Crea actividad
- `completar_actividad(usuario_id, actividad_id)` - Marca como completada
- `obtener_estadisticas_usuario(usuario_id)` - Stats de actividades

---

## Flujo de Datos

### Ejemplo: Usuario completa una misión

```
1️⃣ Frontend envía request POST a /missions/complete
   └─ Datos: usuario_id, mision_id, puntos_obtenidos

2️⃣ Router (mision_router.py) recibe el request
   └─ Llama a HistorialController.registrar_mision_completada()

3️⃣ HistorialController realiza:
   ├─ Verifica que el usuario existe
   ├─ Verifica que la misión existe
   ├─ Registra en historialmisiones
   ├─ Actualiza puntaje del usuario en usuario_controller
   └─ Retorna {"success": true}

4️⃣ Frontend recibe respuesta
   └─ Actualiza UI con nuevos puntos
```

---

## Asociación de Tablas al Usuario

### Las siguientes tablas están asociadas a usuarios:

| Tabla | Campo FK | Controlador | Método de Filtro |
|-------|---------|-------------|-----------------|
| historialmisiones | UsuarioID | HistorialController | `obtener_por_usuario()` |
| progresousuario | UsuarioID | ProgresoController | `obtener_progreso_usuario()` |
| evaluacion | UsuarioID* | EvaluacionController | `obtener_por_usuario()` |
| actividad | UsuarioID* | ActividadController | `obtener_por_usuario()` |

*Nota: Evaluación y Actividad se asocian indirectamente a través de historialmisiones

---

## Mejoras Implementadas

### ✅ 1. Logout Real
- El botón de logout en Navbar ahora limpia:
  - sessionStorage
  - localStorage
  - Cookies
  - Redirecciona a /login

### ✅ 2. Protección de Rutas
- Routes protegidas requieren `usuarioId` en sessionStorage
- Si no existe, redirige automáticamente a /login
- El botón "back" del navegador redirige a login

### ✅ 3. Filtrado por Usuario
- `HistorialController.obtener_por_usuario()` retorna SOLO las misiones de ese usuario
- `EvaluacionController.obtener_por_usuario()` retorna SOLO sus evaluaciones
- `ActividadController.obtener_por_usuario()` retorna SOLO sus actividades
- Las queries SQL incluyen `WHERE UsuarioID = %s`

### ✅ 4. Asociación de Tablas
- historialmisiones: Vincula usuarios con misiones completadas
- progresousuario: Tracking del avance en cada misión
- Evaluaciones y actividades: Asociadas a través del historial

---

## Cómo Usar los Controladores

### Ejemplo en un Router:

```python
from fastapi import APIRouter
from controllers.usuario_controller import UsuarioController
from controllers.mision_controller import MisionController
from controllers.historial_controller import HistorialController

router = APIRouter()

@router.get("/mi-historial/{usuario_id}")
def obtener_mi_historial(usuario_id: int):
    # Obtiene SOLO el historial del usuario actual
    return HistorialController.obtener_por_usuario(usuario_id)

@router.post("/completar-mision")
def completar_mision(usuario_id: int, mision_id: int, puntos: int):
    # Registra que completó la misión
    result = HistorialController.registrar_mision_completada(
        usuario_id=usuario_id,
        mision_id=mision_id,
        puntos_obtenidos=puntos,
        estado_final="Completada"
    )
    return result
```

---

## Próximos Pasos

Si quieres:
1. **Actualizar routers** para usar más controladores - puedo hacerlo
2. **Crear más métodos** en los controladores - avísame qué necesitas
3. **Agregar validaciones** adicionales - por ejemplo, verificar que el usuario solo vea sus datos
4. **Crear reportes** de usuarios - puedo agregar métodos de estadísticas

---

## Resumen

La carpeta `controllers/` centraliza toda la lógica de negocio. Cada controlador:
- Maneja una entidad específica
- Agrupa métodos relacionados
- Garantiza filtrado por usuario donde aplica
- Facilita testing y mantenimiento
- Evita código duplicado

¡Tu proyecto ahora tiene una arquitectura profesional y escalable! 🚀
