from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class SessionCreate(BaseModel):
    user_id: int

class GazeDataIn(BaseModel):
    session_id: int
    fijaciones: int
    sacadas: int
    duracion_media_fijacion: float
    puntos_capturados: int

class SessionFinalize(BaseModel):
    session_id: int
    duracion_segundos: int

class SessionResponse(BaseModel):
    id: int
    user_id: int
    fecha: datetime
    duracion_segundos: Optional[int]
    estado: str

    class Config:
        from_attributes = True