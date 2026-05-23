from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.session import GazeDataIn, SessionFinalize, SessionResponse
from app.services.gaze_service import iniciar_sesion, guardar_gaze, finalizar_sesion
from app.services.ml_service import clasificar_perfil

router = APIRouter(prefix="/sesiones", tags=["sesiones"])

@router.post("/iniciar")
def iniciar(user_id: int, db: Session = Depends(get_db)):
    sesion = iniciar_sesion(db, user_id)
    return {"session_id": sesion.id, "estado": sesion.estado}

@router.post("/guardar-gaze")
def guardar(data: GazeDataIn, db: Session = Depends(get_db)):
    metrica = guardar_gaze(db, data)
    if not metrica:
        raise HTTPException(status_code=400, detail="Error guardando métricas")
    return {"mensaje": "Métricas guardadas", "id": metrica.id}

@router.post("/finalizar")
def finalizar(data: SessionFinalize, db: Session = Depends(get_db)):
    sesion = finalizar_sesion(db, data)
    if not sesion:
        raise HTTPException(status_code=404, detail="Sesión no encontrada")

    resultado = clasificar_perfil(db, data.session_id)
    if not resultado:
        raise HTTPException(status_code=400, detail="Error clasificando perfil")

    return {
        "mensaje": "Sesión finalizada",
        "perfil": resultado.perfil,
        "porcentaje": resultado.porcentaje,
        "confianza": resultado.confianza
    }