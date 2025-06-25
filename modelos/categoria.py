from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from data.database import Base

class Categoria(Base):
    __tablename__ = "categorias"

    categoria_id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)

    # Relación inversa: una categoría tiene muchas tareas
    tareas = relationship("Tarea", back_populates="categoria")

