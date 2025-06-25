from sqlalchemy.orm import Session
from modelos.categoria import Categoria

def insertar_categoria(session: Session, nombre): # Añadido session parameter
    nueva = Categoria(nombre=nombre)
    session.add(nueva)
    session.commit()
    id_insertado = nueva.categoria_id
    # No cerramos la sesión aquí
    return id_insertado

def obtener_categorias(session: Session): # Añadido session parameter
    categorias = session.query(Categoria).all()
    # No cerramos la sesión aquí
    return categorias

def actualizar_categoria(session: Session, categoria_id, nuevo_nombre):
    categoria = session.query(Categoria).filter_by(categoria_id=categoria_id).first()
    if categoria:
        categoria.nombre = nuevo_nombre
        session.commit()
    # No cerramos la sesión aquí

def eliminar_categoria(session: Session, categoria_id):
    session = session # This line is redundant, remove if not doing anything specific
    categoria = session.query(Categoria).filter_by(categoria_id=categoria_id).first()
    if categoria:
        session.delete(categoria)
        session.commit()
    # No cerramos la sesión aquí

