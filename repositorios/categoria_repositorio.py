from sqlalchemy.orm import Session
from modelos.categoria import Categoria
import uuid # Importar uuid para generar IDs

def insertar_categoria(session: Session, nombre: str):
    """
    Inserta una nueva categoría en la base de datos.
    Genera un UUID para categoria_id antes de la inserción.
    :param session: Sesión de SQLAlchemy.
    :param nombre: Nombre de la categoría.
    :return: El ID de la categoría insertada.
    """
    new_categoria_id = str(uuid.uuid4()) # Generar un UUID para la categoría
    nueva = Categoria(categoria_id=new_categoria_id, nombre=nombre) # Pasar el ID generado
    session.add(nueva)
    session.commit() # Confirmar la transacción aquí, ya que inserta y devuelve el ID
    # No cerrar la sesión aquí; dejar que la capa superior lo maneje.
    return new_categoria_id # Devolver el ID generado

def obtener_categorias(session: Session):
    """
    Obtiene todas las categorías de la base de datos.
    :param session: Sesión de SQLAlchemy.
    :return: Lista de objetos Categoria.
    """
    categorias = session.query(Categoria).all()
    # No cerrar la sesión aquí.
    return categorias

def actualizar_categoria(session: Session, categoria_id: str, nuevo_nombre: str):
    """
    Actualiza el nombre de una categoría existente.
    :param session: Sesión de SQLAlchemy.
    :param categoria_id: ID de la categoría a actualizar.
    :param nuevo_nombre: Nuevo nombre de la categoría.
    """
    categoria = session.query(Categoria).filter_by(categoria_id=categoria_id).first()
    if categoria:
        categoria.nombre = nuevo_nombre
        session.commit() # Confirmar la transacción aquí
    # No cerrar la sesión aquí.

def eliminar_categoria(session: Session, categoria_id: str):
    """
    Elimina una categoría de la base de datos.
    :param session: Sesión de SQLAlchemy.
    :param categoria_id: ID de la categoría a eliminar.
    """
    categoria = session.query(Categoria).filter_by(categoria_id=categoria_id).first()
    if categoria:
        session.delete(categoria)
        session.commit() # Confirmar la transacción aquí
    # No cerrar la sesión aquí.
