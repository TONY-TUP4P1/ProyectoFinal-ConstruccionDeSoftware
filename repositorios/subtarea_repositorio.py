from modelos.subtarea import Subtarea


class SubtareaRepositorio:
    def __init__(self, sesion):
        self.sesion = sesion

    def crear(self, subtarea: Subtarea):
        self.sesion.add(subtarea)
        self.sesion.commit()
        return subtarea

    def obtener_por_id(self, subtarea_id: str):
        return self.sesion.query(Subtarea).filter_by(id=subtarea_id).first()

    def listar_por_tarea(self, tarea_id: str):
        return self.sesion.query(Subtarea).filter_by(tarea_id=tarea_id).all()

    def actualizar(self, subtarea: Subtarea):
        self.sesion.commit()
        return subtarea

    def eliminar(self, subtarea: Subtarea):
        self.sesion.delete(subtarea)
        self.sesion.commit()
