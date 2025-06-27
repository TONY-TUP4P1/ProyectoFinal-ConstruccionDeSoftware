from modelos.subtarea import Subtarea
from sqlalchemy.orm import Session # Import Session for type hinting

# ✅ CORRECCIÓN: Usar 'subtarea_id' en la firma y en la creación del objeto
def insertar_subtarea(session: Session, subtarea_id: str, titulo: str, descripcion: str, completada: bool, tarea_id: str):
    """
    Inserta una nueva subtarea en la base de datos.
    :param session: Sesión de SQLAlchemy.
    :param subtarea_id: ID único de la subtarea.
    :param titulo: Título de la subtarea.
    :param descripcion: Descripción de la subtarea.
    :param completada: Estado de la subtarea (True si está completada, False si no).
    :param tarea_id: ID de la tarea a la que pertenece esta subtarea.
    """
    nueva = Subtarea(
        subtarea_id=subtarea_id, # ✅ CORRECCIÓN: Usar 'subtarea_id'
        titulo=titulo,
        descripcion=descripcion,
        completada=completada,
        tarea_id=tarea_id
    )
    session.add(nueva)
    # No session.commit() or session.close() here; let service handle it.

def obtener_subtareas_por_tarea(session: Session, tarea_id: str):
    """
    Obtiene todas las subtareas asociadas a una tarea específica.
    :param session: Sesión de SQLAlchemy.
    :param tarea_id: ID de la tarea.
    :return: Lista de objetos Subtarea.
    """
    subtareas = session.query(Subtarea).filter_by(tarea_id=tarea_id).all()
    return subtareas

# ✅ CORRECCIÓN: Usar 'subtarea_id' en la firma y en el filtro
def actualizar_subtarea(session: Session, subtarea_id: str, **kwargs):
    """
    Actualiza los campos de una subtarea existente.
    :param session: Sesión de SQLAlchemy.
    :param subtarea_id: ID de la subtarea a actualizar.
    :param kwargs: Diccionario de campos a actualizar y sus nuevos valores.
    """
    subtarea = session.query(Subtarea).filter_by(subtarea_id=subtarea_id).first() # ✅ CORRECCIÓN: Usar 'subtarea_id'
    if subtarea:
        for key, value in kwargs.items():
            setattr(subtarea, key, value)
        # No session.commit() or session.close() here; let service handle it.

# ✅ CORRECCIÓN: Usar 'subtarea_id' en la firma y en el filtro
def eliminar_subtarea(session: Session, subtarea_id: str):
    """
    Elimina una subtarea por su ID.
    :param session: Sesión de SQLAlchemy.
    :param subtarea_id: ID de la subtarea a eliminar.
    """
    subtarea = session.query(Subtarea).filter_by(subtarea_id=subtarea_id).first() # ✅ CORRECCIÓN: Usar 'subtarea_id'
    if subtarea:
        session.delete(subtarea)
        # No session.commit() or session.close() here; let service handle it.
