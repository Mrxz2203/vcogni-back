from sqlalchemy.orm import Session
from app.models.gaze_metric import GazeMetric
from app.models.result import Result

def clasificar_perfil(db: Session, session_id: int) -> Result:
    # Obtener métricas de la sesión
    metrica = db.query(GazeMetric).filter(
        GazeMetric.session_id == session_id
    ).first()

    if not metrica:
        return None

    # Clasificación basada en métricas de WebGazer
    # Perfil Visual: fijaciones largas, más fijaciones que sacadas
    # Perfil Verbal: fijaciones cortas, más sacadas que fijaciones
    duracion = metrica.duracion_media_fijacion
    ratio = metrica.fijaciones / max(metrica.sacadas, 1)

    if duracion > 250 and ratio > 1.2:
        perfil = "Visual"
        porcentaje = min(95, 60 + (duracion / 10) + (ratio * 5))
        confianza = min(95, 70 + (duracion / 20))
    else:
        perfil = "Verbal"
        porcentaje = min(95, 60 + ((1 / max(ratio, 0.1)) * 5))
        confianza = min(95, 65 + (metrica.sacadas / 5))

    resultado = Result(
        session_id=session_id,
        perfil=perfil,
        porcentaje=round(porcentaje, 2),
        confianza=round(confianza, 2)
    )
    db.add(resultado)
    db.commit()
    db.refresh(resultado)
    return resultado