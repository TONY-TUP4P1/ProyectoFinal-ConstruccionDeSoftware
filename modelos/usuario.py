from sqlalchemy import Column, String, Date
from sqlalchemy.orm import relationship
from data.database import Base

class Usuario(Base):
    __tablename__ = "usuarios"

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    apellido = Column(String, nullable=False)
    correo = Column(String, unique=True, nullable=False)
    contrasena = Column(String, nullable=False)
    telefono = Column(String)
    fecha_nacimiento = Column(Date)

    # Relación uno-a-muchos: un usuario tiene muchas tareas
    tareas = relationship("Tarea", back_populates="usuario", cascade="all, delete-orphan")

