from sqlalchemy import Column, String, ForeignKey, DateTime, Boolean, Enum, Table
from sqlalchemy.orm import relationship
from data.database import Base
from modelos.tarea import tareas_etiquetas

class Etiqueta(Base):
    __tablename__ = "etiquetas"

    etiqueta_id = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)

    tareas = relationship("Tarea", secondary=tareas_etiquetas, back_populates="etiquetas")

