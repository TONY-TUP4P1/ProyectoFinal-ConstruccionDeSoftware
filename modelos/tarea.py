# modelos/tarea.py

from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from data.database import Base
import enum

# ✅ Define la tabla de asociación ANTES del modelo Tarea
from sqlalchemy import Table

tareas_etiquetas = Table(
    "tareas_etiquetas",
    Base.metadata,
    Column("tarea_id", String, ForeignKey("tareas.tarea_id", ondelete="CASCADE"), primary_key=True),
    Column("etiqueta_id", String, ForeignKey("etiquetas.etiqueta_id", ondelete="CASCADE"), primary_key=True)
)

class PrioridadEnum(enum.Enum):
    ALTA = "ALTA"
    MEDIA = "MEDIA"
    BAJA = "BAJA"

class Tarea(Base):
    __tablename__ = "tareas"

    tarea_id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime)
    fecha_limite = Column(DateTime)
    estado = Column(Boolean, default=False)
    prioridad = Column(Enum(PrioridadEnum), default=PrioridadEnum.MEDIA)

    # CORRECCIÓN: Cambiado 'id' a 'usuario_id' para consistencia con 'ui.py'
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    categoria_id = Column(String, ForeignKey("categorias.categoria_id"))

    usuario = relationship("Usuario", back_populates="tareas")
    categoria = relationship("Categoria", back_populates="tareas")
    subtareas = relationship("Subtarea", back_populates="tarea", cascade="all, delete-orphan")
    etiquetas = relationship("Etiqueta", secondary=tareas_etiquetas, back_populates="tareas")
