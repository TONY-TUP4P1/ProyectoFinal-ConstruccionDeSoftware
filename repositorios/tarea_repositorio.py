from modelos.tarea import Tarea, PrioridadEnum # CORRECTED: Import PrioridadEnum directly
from modelos.etiqueta import Etiqueta # Importa Etiqueta
from data.database import SessionLocal # Keep for reference, but functions will take session
from sqlalchemy.orm import Session # Import Session for type hinting
from datetime import datetime, date # Import necessary for type hints

def insertar_tarea(session: Session, tarea_id: str, titulo: str, descripcion: str, fecha_creacion: datetime,
                   fecha_limite: date, estado: bool, prioridad: PrioridadEnum, usuario_id: str, # CORRECTED: Use PrioridadEnum directly
                   categoria_id: str = None, etiquetas: list[Etiqueta] = None):
    """
    Inserta una nueva tarea en la base de datos.
    :param session: Sesión de SQLAlchemy.
    :param tarea_id: ID único de la tarea.
    :param titulo: Título de la tarea.
    :param descripcion: Descripción de la tarea.
    :param fecha_creacion: Fecha de creación de la tarea.
    :param fecha_limite: Fecha límite de la tarea.
    :param estado: Estado de la tarea (Completada/Pendiente).
    :param prioridad: Prioridad de la tarea (ALTA, MEDIA, BAJA).
    :param usuario_id: ID del usuario al que pertenece la tarea.
    :param categoria_id: ID de la categoría a la que pertenece la tarea (opcional).
    :param etiquetas: Lista de objetos Etiqueta a asociar con la tarea (opcional).
    """
    nueva = Tarea(
        tarea_id=tarea_id,
        titulo=titulo,
        descripcion=descripcion,
        fecha_creacion=fecha_creacion,
        fecha_limite=fecha_limite,
        estado=estado,
        prioridad=prioridad,
        usuario_id=usuario_id, # CORRECCIÓN: Usar usuario_id
        categoria_id=categoria_id
    )
    if etiquetas:
        nueva.etiquetas.extend(etiquetas) # Añadir las etiquetas a la relación

    session.add(nueva)
    # No session.commit() or session.close() here; let service handle it.

def obtener_tareas_por_usuario(session: Session, usuario_id: str, estado: bool = None):
    """
    Obtiene todas las tareas de un usuario específico, opcionalmente filtradas por estado.
    :param session: Sesión de SQLAlchemy.
    :param usuario_id: ID del usuario.
    :param estado: Si se especifica, filtra por estado (True para completadas, False para pendientes).
    :return: Lista de objetos Tarea.
    """
    query = session.query(Tarea).filter_by(usuario_id=usuario_id)
    if estado is not None:
        query = query.filter_by(estado=estado)
    tareas = query.all()
    return tareas

def obtener_tarea_por_id(session: Session, tarea_id: str):
    """
    Obtiene una tarea por su ID.
    :param session: Sesión de SQLAlchemy.
    :param tarea_id: ID de la tarea.
    :return: Objeto Tarea o None si no se encuentra.
    """
    tarea = session.query(Tarea).filter_by(tarea_id=tarea_id).first()
    return tarea

def actualizar_tarea(session: Session, tarea_id: str, **kwargs):
    """
    Actualiza los campos de una tarea existente.
    :param session: Sesión de SQLAlchemy.
    :param tarea_id: ID de la tarea a actualizar.
    :param kwargs: Diccionario de campos a actualizar y sus nuevos valores.
                   Puede incluir 'etiquetas' como una lista de objetos Etiqueta.
    """
    tarea = session.query(Tarea).filter_by(tarea_id=tarea_id).first()
    if tarea:
        # Manejar la actualización de la relación de etiquetas por separado
        if 'etiquetas' in kwargs:
            tarea.etiquetas.clear() # Limpiar las etiquetas existentes
            tarea.etiquetas.extend(kwargs.pop('etiquetas')) # Añadir las nuevas etiquetas
            
        for clave, valor in kwargs.items():
            setattr(tarea, clave, valor)
        # No session.commit() or session.close() here; let service handle it.

def eliminar_tarea_por_id(session: Session, tarea_id: str):
    """
    Elimina una tarea por su ID.
    :param session: Sesión de SQLAlchemy.
    :param tarea_id: ID de la tarea a eliminar.
    """
    tarea = session.query(Tarea).filter_by(tarea_id=tarea_id).first()
    if tarea:
        session.delete(tarea)
        # No session.commit() or session.close() here; let service handle it.
