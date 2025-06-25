from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from modelos.base import Base

class Categoria(Base):
    __tablename__ = 'categorias'

    id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)

    tareas = relationship("Tarea", back_populates="categoria")
