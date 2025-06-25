from sqlalchemy.orm import Session
from modelos.subtarea import Subtarea
from repositorios.subtarea_repositorio import (
    insertar_subtarea,
    obtener_subtareas_por_tarea,
    actualizar_subtarea,
    eliminar_subtarea
)

class SubtareaService:
    def __init__(self, session: Session):
        self.session = session

    def crear_subtarea(self, subtarea: Subtarea):
        """Crea una nueva subtarea y la guarda en la base de datos."""
        try:
            insertar_subtarea(
                self.session, # Pasa la sesión al repositorio
                subtarea.subatarea_id,
                subtarea.titulo,
                subtarea.descripcion,
                subtarea.completada,
                subtarea.tarea_id
            )
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al crear subtarea: {e}")
            return False


    def listar_por_tarea(self, tarea_id: str):
        """Lista las subtareas de una tarea específica."""
        return obtener_subtareas_por_tarea(self.session, tarea_id)

    def actualizar_subtarea(self, subatarea_id: str, **kwargs):
        """Actualiza una subtarea existente."""
        try:
            actualizar_subtarea(self.session, subatarea_id, **kwargs) # Pasa la sesión
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar subtarea: {e}")
            return False

    def eliminar_subtarea(self, subatarea_id: str):
        """Elimina una subtarea por su ID."""
        try:
            eliminar_subtarea(self.session, subatarea_id) # Pasa la sesión
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar subtarea: {e}")
            return False

