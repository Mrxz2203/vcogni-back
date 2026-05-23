from sqlalchemy.orm import Session
from app.models.session import Session as SessionModel
from app.models.gaze_metric import GazeMetric
from app.models.result import Result
from app.schemas.session import GazeDataIn, SessionFinalize

def iniciar_sesion(db: Session, user_id: int) -> SessionModel:
    sesion = SessionModel(user_id=user_id, estado="en_progreso")
    db.add(sesion)
    db.commit()
    db.refresh(sesion)
    return sesion

def guardar_gaze(db: Session, data: GazeDataIn) -> GazeMetric:
    metrica = GazeMetric(
        session_id=data.session_id,
        fijaciones=data.fijaciones,
        sacadas=data.sacadas,
        duracion_media_fijacion=data.duracion_media_fijacion,
        puntos_capturados=data.puntos_capturados
    )
    db.add(metrica)
    db.commit()
    db.refresh(metrica)
    return metrica

def finalizar_sesion(db: Session, data: SessionFinalize) -> SessionModel:
    sesion = db.query(SessionModel).filter(SessionModel.id == data.session_id).first()
    if not sesion:
        return None
    sesion.duracion_segundos = data.duracion_segundos
    sesion.estado = "completada"
    db.commit()
    db.refresh(sesion)
    return sesion