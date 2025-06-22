from modelos.subtarea import Subtarea
from repositorios.subtarea_repositorio import SubtareaRepositorio
from repositorios.tarea_repositorio import TareaRepositorio


class SubtareaServicio:
    def __init__(
            self,
            subtarea_repo: SubtareaRepositorio,
            tarea_repo: TareaRepositorio):
        self.subtarea_repo = subtarea_repo
        self.tarea_repo = tarea_repo

    def crear_subtarea(self, tarea_id, titulo, descripcion=None):
        if not titulo:
            raise ValueError("La subtarea debe tener un título.")
        if not self.tarea_repo.obtener_por_id(tarea_id):
            raise ValueError("La tarea asociada no existe.")

        nueva_subtarea = Subtarea(
            tarea_id=tarea_id,
            titulo=titulo,
            descripcion=descripcion,
            completada=False
        )
        return self.subtarea_repo.crear(nueva_subtarea)

    def completar_subtarea(self, subtarea_id):
        subtarea = self.subtarea_repo.obtener_por_id(subtarea_id)
        if not subtarea:
            raise ValueError("Subtarea no encontrada.")
        subtarea.completada = True
        return self.subtarea_repo.actualizar(subtarea)
