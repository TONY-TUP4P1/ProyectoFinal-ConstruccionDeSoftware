from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship
from modelos.base import Base

class Usuario(Base):
    __tablename__ = 'usuarios'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    contrasena = Column(String, nullable=False)
    correo = Column(String, nullable=False)
    telefono = Column(String, nullable=False)
    fecha_nacimiento = Column(DateTime, nullable=False)

    tareas = relationship("Tarea", back_populates="usuario", cascade="all, delete-orphan")
