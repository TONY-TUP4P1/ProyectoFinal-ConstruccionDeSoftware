from modelos.categoria import Categoria


class CategoriaRepositorio:
    def __init__(self, sesion):
        self.sesion = sesion

    def crear(self, categoria: Categoria):
        self.sesion.add(categoria)
        self.sesion.commit()
        return categoria

    def obtener_por_id(self, categoria_id: str):
        return self.sesion.query(Categoria).filter_by(id=categoria_id).first()

    def obtener_por_nombre(self, nombre: str):
        return self.sesion.query(Categoria).filter_by(nombre=nombre).first()

    def listar(self):
        return self.sesion.query(Categoria).all()

    def eliminar(self, categoria: Categoria):
        self.sesion.delete(categoria)
        self.sesion.commit()
