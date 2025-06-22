from datetime import datetime

from modelos.tarea import Tarea
from repositorios.tarea_repositorio import TareaRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio


class TareaServicio:
    def __init__(self, tarea_repo: TareaRepositorio,
                 usuario_repo: UsuarioRepositorio):
        self.tarea_repo = tarea_repo
        self.usuario_repo = usuario_repo

    def crear_tarea(
            self,
            usuario_id,
            titulo,
            descripcion=None,
            fecha_limite=None,
            estado=False,
            prioridad=None):
        if not titulo:
            raise ValueError("El título de la tarea es obligatorio.")

        if not self.usuario_repo.obtener_por_id(usuario_id):
            raise ValueError("El usuario asociado no existe.")

        nueva_tarea = Tarea(
            usuario_id=usuario_id,
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=datetime.now(),
            fecha_limite=fecha_limite,
            estado=estado,
            prioridad = prioridad
        )
        return self.tarea_repo.crear(nueva_tarea)

    def obtener_tareas_de_usuario(self, usuario_id: str):
        return self.tarea_repo.listar_por_usuario(usuario_id)

    def marcar_completada(self, tarea_id: str):
        tarea = self.tarea_repo.obtener_por_id(tarea_id)
        if not tarea:
            raise ValueError("Tarea no encontrada.")
        tarea.estado = True
        return self.tarea_repo.actualizar(tarea)

    def obtener_tareas_por_estado(self, usuario_id, completada: bool):
        return self.tarea_repo.listar_por_estado(usuario_id, completada)

    def obtener_tareas_que_vencen_hoy(self, usuario_id):
        return self.tarea_repo.listar_por_fecha_limite_hoy(usuario_id)

    def obtener_tareas_por_rango(self, usuario_id, fecha_inicio, fecha_fin):
        return self.tarea_repo.listar_por_rango_fecha(
            usuario_id, fecha_inicio, fecha_fin)
