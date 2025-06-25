from sqlalchemy.orm import Session
from modelos.categoria import Categoria
from repositorios.categoria_repositorio import (
    insertar_categoria,
    obtener_categorias,
    actualizar_categoria,
    eliminar_categoria
)

class CategoriaService:
    def __init__(self, session: Session):
        self.session = session

    def asignar_categoria(self, nombre: str) -> str: # Cambiado a str, asumo que categoria_id es TEXT
        return insertar_categoria(self.session, nombre) # Pasa la sesión

    def listar_categorias(self):
        return obtener_categorias(self.session) # Pasa la sesión

    def actualizar_categoria(self, categoria_id: str, nuevo_nombre: str): # Cambiado a str
        actualizar_categoria(self.session, categoria_id, nuevo_nombre)

    def eliminar_categoria(self, categoria_id: str): # Cambiado a str
        eliminar_categoria(self.session, categoria_id)

