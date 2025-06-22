import enum
import uuid

from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base
from .tareas_etiquetas import tareas_etiquetas


class NivelPrioridad(enum.Enum):
    ALTA = "Alta"
    MEDIA = "Media"
    BAJA = "Baja"


class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime)
    fecha_limite = Column(DateTime)
    estado = Column(Boolean, default=False)
    prioridad = Column(Enum(NivelPrioridad), default=NivelPrioridad.MEDIA)
    usuario_id = Column(String, ForeignKey("usuarios.id"))
    categoria_id = Column(String, ForeignKey("categorias.id"), nullable=True)

    usuarios = relationship("Usuario", back_populates="tareas")
    subtareas = relationship(
        "Subtarea",
        back_populates="tarea",
        cascade="all, delete-orphan")
    categoria = relationship("Categoria", back_populates="tareas")
    etiquetas = relationship(
        "Etiqueta",
        secondary=tareas_etiquetas,
        back_populates="tareas")
