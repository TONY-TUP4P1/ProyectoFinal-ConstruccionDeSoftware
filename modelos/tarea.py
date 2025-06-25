from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Enum
import enum
from sqlalchemy.orm import relationship
from modelos.base import Base

class PrioridadEnum(enum.Enum):
    baja = "baja"
    media = "media"
    alta = "alta"

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    fecha_creacion = Column(DateTime, nullable=False)
    fecha_limite = Column(DateTime, nullable=False)
    estado = Column(Boolean, nullable=False)
    prioridad = Column(Enum(PrioridadEnum), nullable=False, default=PrioridadEnum.media)


    usuario_id = Column(String, ForeignKey('usuarios.id'), nullable=False)
    usuario = relationship("Usuario", back_populates="tareas")

    subtareas = relationship("SubTarea", back_populates="tarea", cascade="all, delete-orphan")
    etiquetas = relationship("Etiqueta", back_populates="tarea", cascade="all, delete-orphan")

    categoria_id = Column(String, ForeignKey('categorias.id'), nullable=True)
    categoria = relationship("Categoria", back_populates="tareas")

