from modelos.etiqueta import Etiqueta
from data.database import SessionLocal # Keep for reference, but functions will take session
from sqlalchemy.orm import Session # Import Session for type hinting

def insertar_etiqueta(session: Session, etiqueta_id: str, nombre: str):
    """Inserta una nueva etiqueta en la base de datos."""
    nueva = Etiqueta(etiqueta_id=etiqueta_id, nombre=nombre)
    session.add(nueva)
    # No session.commit() or session.close() here; let service handle it.

def obtener_etiquetas(session: Session):
    """Obtiene todas las etiquetas de la base de datos."""
    etiquetas = session.query(Etiqueta).all()
    return etiquetas

def obtener_etiqueta_por_nombre(session: Session, nombre: str):
    """Obtiene una etiqueta por su nombre."""
    return session.query(Etiqueta).filter_by(nombre=nombre).first()

def actualizar_etiqueta(session: Session, etiqueta_id: str, nuevo_nombre: str):
    """Actualiza el nombre de una etiqueta existente."""
    etiqueta = session.query(Etiqueta).filter_by(etiqueta_id=etiqueta_id).first()
    if etiqueta:
        etiqueta.nombre = nuevo_nombre
        # No session.commit() or session.close() here; let service handle it.

def eliminar_etiqueta(session: Session, etiqueta_id: str):
    """Elimina una etiqueta de la base de datos."""
    etiqueta = session.query(Etiqueta).filter_by(etiqueta_id=etiqueta_id).first()
    if etiqueta:
        session.delete(etiqueta)
        # No session.commit() or session.close() here; let service handle it.
