from modelos.usuario import Usuario
from repositorios.usuario_repositorio import crear_usuario, obtener_usuario
from sqlalchemy.orm import Session

def registrar_usuario(db: Session, nombre_usuario: str, correo: str):
    return crear_usuario(db, nombre_usuario, correo)

def obtener_perfil_usuario(db: Session, usuario_id: int):
    return obtener_usuario(db, usuario_id)


def registrar_usuario(db: Session, nombre_usuario: str, correo: str):
    if not nombre_usuario or not nombre_usuario.strip():
        raise ValueError("El nombre de usuario es obligatorio.")
    if not correo or not correo.strip():
        raise ValueError("El correo es obligatorio.")
    if db.query(Usuario).filter(Usuario.correo == correo).first():
        raise ValueError("Ya existe un usuario con ese correo.")
    if db.query(Usuario).filter(Usuario.nombre_usuario == nombre_usuario).first():
        raise ValueError("Ya existe un usuario con ese nombre de usuario.")

    return crear_usuario(db, nombre_usuario.strip(), correo.strip())

def obtener_perfil_usuario(db: Session, usuario_id: int):
    usuario = obtener_usuario(db, usuario_id)
    if not usuario:
        raise ValueError(f"No se encontró el usuario con ID {usuario_id}.")
    return usuario
