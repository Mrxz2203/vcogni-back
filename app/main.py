from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, sessions, results
from app.core.database import engine, Base

# Crear tablas automáticamente
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="V-COGNI API",
    description="Backend para el sistema de identificación de estilos cognitivos",
    version="1.0.0"
)

# CORS para que React pueda conectarse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(sessions.router)
app.include_router(results.router)

@app.get("/")
def root():
    return {"mensaje": "V-COGNI API corriendo", "version": "1.0.0"}