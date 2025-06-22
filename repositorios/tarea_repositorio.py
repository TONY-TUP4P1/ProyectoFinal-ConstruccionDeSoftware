from datetime import datetime, timedelta

from modelos.tarea import Tarea


class TareaRepositorio:
    def __init__(self, sesion):
        self.sesion = sesion

    def crear(self, tarea: Tarea):
        self.sesion.add(tarea)
        self.sesion.commit()
        return tarea

    def obtener_por_id(self, tarea_id: str):
        return self.sesion.query(Tarea).filter_by(id=tarea_id).first()

    def listar_por_usuario(self, usuario_id: str):
        return self.sesion.query(Tarea).filter_by(usuario_id=usuario_id).all()

    def actualizar(self, tarea: Tarea):
        self.sesion.commit()
        return tarea

    def eliminar(self, tarea: Tarea):
        self.sesion.delete(tarea)
        self.sesion.commit()

    def listar_por_estado(self, usuario_id, completada: bool):
        return self.sesion.query(Tarea).filter_by(
            usuario_id=usuario_id, estado=completada).all()

    def listar_por_fecha_limite_hoy(self, usuario_id):
        hoy = datetime.now().date()
        return self.sesion.query(Tarea).filter(
            Tarea.usuario_id == usuario_id,
            Tarea.fecha_limite is not None,
            Tarea.fecha_limite <= hoy
        ).all()

    def listar_por_rango_fecha(self, usuario_id, fecha_inicio, fecha_fin):
        return self.sesion.query(Tarea).filter(
            Tarea.usuario_id == usuario_id,
            Tarea.fecha_limite.between(fecha_inicio, fecha_fin)
        ).all()
