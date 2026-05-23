from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.result import Result
from app.models.session import Session as SessionModel
from app.schemas.result import ResultResponse, HistorialItem
from typing import List

router = APIRouter(prefix="/resultados", tags=["resultados"])

@router.get("/ultimo/{user_id}", response_model=ResultResponse)
def ultimo_resultado(user_id: int, db: Session = Depends(get_db)):
    resultado = db.query(Result).join(SessionModel).filter(
        SessionModel.user_id == user_id
    ).order_by(Result.created_at.desc()).first()

    if not resultado:
        raise HTTPException(status_code=404, detail="No hay resultados aún")
    return resultado

@router.get("/historial/{user_id}", response_model=List[HistorialItem])
def historial(user_id: int, db: Session = Depends(get_db)):
    sesiones = db.query(SessionModel).filter(
        SessionModel.user_id == user_id,
        SessionModel.estado == "completada"
    ).order_by(SessionModel.fecha.desc()).all()

    historial = []
    for s in sesiones:
        if s.result:
            historial.append(HistorialItem(
                session_id=s.id,
                fecha=s.fecha,
                perfil=s.result.perfil,
                porcentaje=s.result.porcentaje,
                confianza=s.result.confianza,
                duracion_segundos=s.duracion_segundos
            ))
    return historial

@router.get("/perfil/{user_id}")
def perfil_usuario(user_id: int, db: Session = Depends(get_db)):
    from app.models.user import User
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {
        "id": usuario.id,
        "nombre": usuario.nombre,
        "codigo": usuario.codigo,
        "carrera": usuario.carrera,
        "rol": usuario.rol
    }

@router.put("/perfil/{user_id}")
def actualizar_perfil(user_id: int, nombre: str, carrera: str, db: Session = Depends(get_db)):
    from app.models.user import User
    usuario = db.query(User).filter(User.id == user_id).first()
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    usuario.nombre = nombre
    usuario.carrera = carrera
    db.commit()
    db.refresh(usuario)
    return {"mensaje": "Perfil actualizado", "nombre": usuario.nombre}