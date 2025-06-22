from modelos.etiqueta import Etiqueta


class EtiquetaRepositorio:
    def __init__(self, sesion):
        self.sesion = sesion

    def crear(self, etiqueta: Etiqueta):
        self.sesion.add(etiqueta)
        self.sesion.commit()
        return etiqueta

    def obtener_por_id(self, etiqueta_id: str):
        return self.sesion.query(Etiqueta).filter_by(id=etiqueta_id).first()

    def obtener_por_nombre(self, nombre: str):
        return self.sesion.query(Etiqueta).filter_by(nombre=nombre).first()

    def listar(self):
        return self.sesion.query(Etiqueta).all()

    def eliminar(self, etiqueta: Etiqueta):
        self.sesion.delete(etiqueta)
        self.sesion.commit()
