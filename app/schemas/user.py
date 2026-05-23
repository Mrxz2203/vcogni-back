from pydantic import BaseModel
from typing import Optional
from enum import Enum

class RolEnum(str, Enum):
    estudiante = "estudiante"
    docente = "docente"
    admin = "admin"

# Registro
class UserCreate(BaseModel):
    nombre: str
    codigo: str
    password: str
    rol: RolEnum = RolEnum.estudiante
    carrera: Optional[str] = None

# Login
class UserLogin(BaseModel):
    codigo: str
    password: str

# Respuesta (sin password)
class UserResponse(BaseModel):
    id: int
    nombre: str
    codigo: str
    rol: RolEnum
    carrera: Optional[str] = None

    class Config:
        from_attributes = True

# Token JWT
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    rol: str
    nombre: str
    user_id: int