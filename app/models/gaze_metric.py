from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class GazeMetric(Base):
    __tablename__ = "gaze_metrics"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id"), nullable=False)
    fijaciones = Column(Integer, default=0)
    sacadas = Column(Integer, default=0)
    duracion_media_fijacion = Column(Float, default=0.0)
    puntos_capturados = Column(Integer, default=0)

    session = relationship("Session", back_populates="gaze_metrics")