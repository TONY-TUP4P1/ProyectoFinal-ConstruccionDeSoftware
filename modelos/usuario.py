from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(Integer, primary_key=True)
    nombre_usuario = Column(String, unique=True, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    tareas = relationship("Tarea", back_populates="usuario")