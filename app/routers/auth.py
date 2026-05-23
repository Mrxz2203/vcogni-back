from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.schemas.user import UserCreate, UserLogin, Token
from app.services.auth_service import crear_usuario, login_usuario, generar_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/registro")
def registro(data: UserCreate, db: Session = Depends(get_db)):
    usuario = crear_usuario(db, data)
    if not usuario:
        raise HTTPException(status_code=400, detail="El código institucional ya está registrado")
    return {"mensaje": "Usuario registrado correctamente", "id": usuario.id}

@router.post("/login", response_model=Token)
def login(data: UserLogin, db: Session = Depends(get_db)):
    usuario = login_usuario(db, data.codigo, data.password)
    if not usuario:
        raise HTTPException(status_code=401, detail="Código o contraseña incorrectos")
    return generar_token(usuario)