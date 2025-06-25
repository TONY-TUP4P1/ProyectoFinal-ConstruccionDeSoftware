from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from modelos.base import Base

class Etiqueta(Base):
    __tablename__ = 'etiquetas'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)

    tarea_id = Column(String, ForeignKey('tareas.id'), nullable=False)
    tarea = relationship("Tarea", back_populates="etiquetas")
