from modelos.usuario import Usuario
from sqlalchemy.orm import Session

def crear_usuario(db: Session, nombre_usuario: str, correo: str):
    db_usuario = Usuario(nombre_usuario=nombre_usuario, correo=correo)
    db.add(db_usuario)
    db.commit()
    db.refresh(db_usuario)
    return db_usuario

def obtener_usuario(db: Session, usuario_id: int):
    return db.query(Usuario).filter(Usuario.id == usuario_id).first()
