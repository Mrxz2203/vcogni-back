from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from app.core.database import Base

class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)
    duracion_segundos = Column(Integer, nullable=True)
    estado = Column(String, default="en_progreso")

    user = relationship("User", back_populates="sessions")
    gaze_metrics = relationship("GazeMetric", back_populates="session")
    result = relationship("Result", back_populates="session", uselist=False)