from modelos.categoria import Categoria
from repositorios.categoria_repositorio import CategoriaRepositorio


class CategoriaServicio:
    def __init__(self, categoria_repo: CategoriaRepositorio):
        self.categoria_repo = categoria_repo

    def crear_categoria(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre de la categoría es obligatorio.")
        if self.categoria_repo.obtener_por_nombre(nombre):
            raise ValueError("La categoría ya existe.")
        nueva_categoria = Categoria(nombre=nombre)
        return self.categoria_repo.crear(nueva_categoria)

    def listar_categorias(self):
        return self.categoria_repo.listar()

    def obtener_categoria(self, categoria_id: str):
        categoria = self.categoria_repo.obtener_por_id(categoria_id)
        if not categoria:
            raise ValueError("Categoría no encontrada.")
        return categoria
