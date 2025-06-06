from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Tarea(Base):
    __tablename__ = 'tareas'

    id = Column(Integer, primary_key=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    fecha_creacion = Column(DateTime)
    fecha_limite = Column(DateTime)
    completada = Column(Boolean, default=False)
    usuario_id = Column(Integer, ForeignKey('usuarios.id'))
    usuario = relationship("Usuario", back_populates="tareas")