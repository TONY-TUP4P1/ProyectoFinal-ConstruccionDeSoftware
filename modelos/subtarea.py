import uuid

from sqlalchemy import Boolean, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from .base import Base


class Subtarea(Base):
    __tablename__ = "subtareas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    completada = Column(Boolean, default=False)

    tarea_id = Column(String, ForeignKey("tareas.id"), nullable=False)

    tarea = relationship("Tarea", back_populates="subtareas")
