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

from .usuario_repositorio import UsuarioRepository
from .tarea_repositorio import TareaRepository
from .subtarea_repositorio import SubTareaRepository
from .etiqueta_repositorio import EtiquetaRepository
from .categoria_repositorio import CategoriaRepository

