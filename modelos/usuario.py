from sqlalchemy import Column, String, Date, Integer
from sqlalchemy.orm import relationship

from database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    telefono = Column(String)
    fecha_nacimiento = Column(Date)
    tareas = relationship("Tarea", back_populates="usuario")  # ✅
