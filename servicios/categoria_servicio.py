from sqlalchemy.orm import Session
from modelos.categoria import Categoria
from repositorios.categoria_repositorio import CategoriaRepository

class CategoriaService:
    def __init__(self, session: Session):
        self.repo = CategoriaRepository(session)

    def asignar_categoria(self, categoria: Categoria):
        self.repo.create(categoria)

    def eliminar_categoria(self, categoria_id: str):
        self.repo.delete(categoria_id)
