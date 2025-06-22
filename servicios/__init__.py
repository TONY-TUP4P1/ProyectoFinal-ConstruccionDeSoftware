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

from .categoria_servicio import CategoriaServicio
from .etiqueta_servicio import EtiquetaServicio
from .subtarea_servicio import SubtareaServicio
from .tarea_servicio import TareaServicio
from .usuario_servicio import UsuarioServicio
