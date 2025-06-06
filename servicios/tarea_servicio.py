from modelos.usuario import Usuario
from modelos.tarea import Tarea
from repositorios.tarea_repositorio import crear_tarea, obtener_tareas, actualizar_tarea, eliminar_tarea
from sqlalchemy.orm import Session

def crear_nueva_tarea(db: Session, nombre: str, descripcion: str, usuario_id: int):
    return crear_tarea(db, nombre, descripcion, usuario_id)

def ver_tareas_usuario(db: Session, usuario_id: int):
    return obtener_tareas(db, usuario_id)

def marcar_tarea_como_completada(db: Session, tarea_id: int):
    return actualizar_tarea(db, tarea_id, True)

def eliminar_una_tarea(db: Session, tarea_id: int):
    return eliminar_tarea(db, tarea_id)


def crear_nueva_tarea(db: Session, nombre: str, descripcion: str, usuario_id: int):
    if not nombre or not nombre.strip():
        raise ValueError("El nombre de la tarea es obligatorio.")
    if not descripcion or not descripcion.strip():
        raise ValueError("La descripción de la tarea es obligatoria.")
    if not db.query(Usuario).filter(Usuario.id == usuario_id).first():
        raise ValueError(f"No existe un usuario con ID {usuario_id}.")

    return crear_tarea(db, nombre.strip(), descripcion.strip(), usuario_id)

def ver_tareas_usuario(db: Session, usuario_id: int):
    if not db.query(Usuario).filter(Usuario.id == usuario_id).first():
        raise ValueError(f"No existe un usuario con ID {usuario_id}.")
    return obtener_tareas(db, usuario_id)


def marcar_tarea_como_completada(db: Session, tarea_id: int):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise ValueError(f"No existe una tarea con ID {tarea_id}.")
    if tarea.completada:
        raise ValueError("La tarea ya está marcada como completada.")

    return actualizar_tarea(db, tarea_id, True)


def eliminar_una_tarea(db: Session, tarea_id: int):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise ValueError(f"No existe una tarea con ID {tarea_id}.")

    return eliminar_tarea(db, tarea_id)
