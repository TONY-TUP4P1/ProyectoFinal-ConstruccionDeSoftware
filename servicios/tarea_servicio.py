from sqlalchemy.orm import Session
from modelos.tarea import Tarea
from repositorios.tarea_repositorio import TareaRepository

class TareaService:
    def __init__(self, session: Session):
        self.repo = TareaRepository(session)

    def crear_tarea(self, tarea: Tarea):
        self.repo.create(tarea)

    def obtener_tarea(self, tarea_id: str):
        return self.repo.read(tarea_id)

    def finalizar_tarea(self, tarea_id: str):
        tarea = self.repo.read(tarea_id)
        if tarea:
            tarea.estado = True
            self.repo.update(tarea)

    def eliminar_tarea(self, tarea_id: str):
        self.repo.delete(tarea_id)
