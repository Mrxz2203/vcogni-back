from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ResultResponse(BaseModel):
    id: int
    session_id: int
    perfil: str
    porcentaje: float
    confianza: float
    created_at: datetime

    class Config:
        from_attributes = True

class HistorialItem(BaseModel):
    session_id: int
    fecha: datetime
    perfil: str
    porcentaje: float
    confianza: float
    duracion_segundos: Optional[int]

    class Config:
        from_attributes = True