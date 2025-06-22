import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base


class Categoria(Base):
    __tablename__ = "categorias"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)

    tareas = relationship("Tarea", back_populates="categoria")
