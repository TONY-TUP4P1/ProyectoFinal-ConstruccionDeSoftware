"""
repositorios package

Implementa la capa de acceso a datos. Cada repositorio contiene métodos CRUD para una entidad
específica, utilizando SQLAlchemy para interactuar con la base de datos.

Repositorio por entidad:
    - UsuarioRepositorio
    - TareaRepositorio
    - SubtareaRepositorio
    - CategoriaRepositorio
    - EtiquetaRepositorio
"""

from .categoria_repositorio import CategoriaRepositorio
from .etiqueta_repositorio import EtiquetaRepositorio
from .subtarea_repositorio import SubtareaRepositorio
from .tarea_repositorio import TareaRepositorio
from .usuario_repositorio import UsuarioRepositorio
