from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import (
    usuario_router,
    progreso_router,
    notificacion_router,
    mision_router,
    evaluacion_router,
    recomendacion_router,
    dolarvalor_router,
    actividad_router,
    historial_router,
    recuperacion_router,
    actividad_usuario_router
)

app = FastAPI()

# Lista de orígenes permitidos (⚙️ incluye 5174)
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",      # ✅ agrega este
    "http://127.0.0.1:5174",     # ✅ y este
    "http://localhost:3001",
    "http://127.0.0.1:3001"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Registro de routers
app.include_router(usuario_router.router)
app.include_router(progreso_router.router)
app.include_router(notificacion_router.router)
app.include_router(mision_router.router)
app.include_router(evaluacion_router.router)
app.include_router(recomendacion_router.router)
app.include_router(dolarvalor_router.router)
app.include_router(actividad_router.router)
app.include_router(historial_router.router)
app.include_router(recuperacion_router.router)
app.include_router(actividad_usuario_router.router)

@app.get("/")
def root():
    return {"message": "🚀 API CreditWise funcionando correctamente"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
