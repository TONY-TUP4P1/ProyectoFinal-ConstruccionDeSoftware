from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from data.database import Base

class Subtarea(Base):
    __tablename__ = "subtareas"

    subtarea_id = Column(String, primary_key=True) # Corregido de subatarea_id
    titulo = Column(String, nullable=False)
    descripcion = Column(String)
    completada = Column(Boolean, default=False)
    
    tarea_id = Column(String, ForeignKey("tareas.tarea_id"), nullable=False)

    tarea = relationship("Tarea", back_populates="subtareas")

