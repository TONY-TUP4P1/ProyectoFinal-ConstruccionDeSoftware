from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from modelos.base import Base

class SubTarea(Base):
    __tablename__ = 'subtareas'

    id = Column(String, primary_key=True)
    titulo = Column(String, nullable=False)
    descripcion = Column(String, nullable=False)
    completada = Column(Boolean, nullable=False)

    tarea_id = Column(String, ForeignKey('tareas.id'), nullable=False)
    tarea = relationship("Tarea", back_populates="subtareas")
