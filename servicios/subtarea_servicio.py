from sqlalchemy.orm import Session
from modelos.subtarea import SubTarea
from repositorios.subtarea_repositorio import SubTareaRepository

class SubTareaService:
    def __init__(self, session: Session):
        self.repo = SubTareaRepository(session)

    def crear_subtarea(self, subtarea: SubTarea):
        self.repo.create(subtarea)

    def marcar_completada(self, subtarea_id: str):
        subtarea = self.repo.read(subtarea_id)
        if subtarea:
            subtarea.completada = True
            self.repo.update(subtarea)

    def eliminar_subtarea(self, subtarea_id: str):
        self.repo.delete(subtarea_id)
