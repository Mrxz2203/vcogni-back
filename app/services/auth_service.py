from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import hash_password, verify_password, create_access_token

def crear_usuario(db: Session, data: UserCreate):
    # Verificar si el código ya existe
    existe = db.query(User).filter(User.codigo == data.codigo).first()
    if existe:
        return None

    usuario = User(
        nombre=data.nombre,
        codigo=data.codigo,
        password=hash_password(data.password),
        rol=data.rol,
        carrera=data.carrera
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario

def login_usuario(db: Session, codigo: str, password: str):
    usuario = db.query(User).filter(User.codigo == codigo).first()
    if not usuario:
        return None
    if not verify_password(password, usuario.password):
        return None
    return usuario

def generar_token(usuario: User) -> dict:
    token = create_access_token({
        "sub": str(usuario.id),
        "rol": usuario.rol,
        "nombre": usuario.nombre
    })
    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "nombre": usuario.nombre,
        "user_id": usuario.id
    }