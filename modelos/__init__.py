"""
models package

Contiene las definiciones de los modelos ORM usados en la base de datos del sistema.
Incluye entidades como Usuario, Tarea, Subtarea, Etiqueta, Categoría y su relación N:M.

Todos los modelos son registrados a través del objeto Base para crear las tablas correspondientes.
"""

# modelos/__init__.py
from .base import Base
from .tarea import Tarea
from .usuario import Usuario  # <-- Usuario después de Tarea
from .subtarea import Subtarea
from .etiqueta import Etiqueta
from .categoria import Categoria
from .tareas_etiquetas import tareas_etiquetas

