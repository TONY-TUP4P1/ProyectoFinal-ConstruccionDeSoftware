"""
servicios package

Contiene la lógica de negocio del sistema. Los servicios actúan como intermediarios entre la
interfaz de usuario y los repositorios, aplicando validaciones y reglas.

Servicios por entidad:
    - UsuarioServicio
    - TareaServicio
    - SubtareaServicio
    - CategoriaServicio
    - EtiquetaServicio
"""

from .usuario_servicio import UsuarioService
from .tarea_servicio import TareaService
from .subtarea_servicio import SubTareaService
from .etiqueta_servicio import EtiquetaService
from .categoria_servicio import CategoriaService

