from modelos.tarea import Tarea
from sqlalchemy.orm import Session

def crear_tarea(db: Session, nombre: str, descripcion: str, usuario_id: int):
    db_tarea = Tarea(nombre=nombre, descripcion=descripcion, usuario_id=usuario_id)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def obtener_tareas(db: Session, usuario_id: int):
    return db.query(Tarea).filter(Tarea.usuario_id == usuario_id).all()

def actualizar_tarea(db: Session, tarea_id: int, completada: bool):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    db_tarea.completada = completada
    db.commit()
    return db_tarea

def eliminar_tarea(db: Session, tarea_id: int):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    db.delete(db_tarea)
    db.commit()
    return db_tarea