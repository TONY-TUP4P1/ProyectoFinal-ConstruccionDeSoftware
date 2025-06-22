import uuid

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from .base import Base
from .tareas_etiquetas import tareas_etiquetas


class Etiqueta(Base):
    __tablename__ = "etiquetas"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    nombre = Column(String, nullable=False)

    tareas = relationship(
        "Tarea",
        secondary=tareas_etiquetas,
        back_populates="etiquetas")
