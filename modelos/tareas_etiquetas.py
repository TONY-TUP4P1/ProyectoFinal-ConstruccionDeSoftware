from sqlalchemy import Column, ForeignKey, String, Table

from .base import Base

tareas_etiquetas = Table(
    "tareas_etiquetas", Base.metadata, Column(
        "tarea_id", String, ForeignKey(
            "tareas.id", ondelete="CASCADE"), primary_key=True), Column(
                "etiqueta_id", String, ForeignKey(
                    "etiquetas.id", ondelete="CASCADE"), primary_key=True))
