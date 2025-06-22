from modelos.usuario import Usuario


class UsuarioRepositorio:
    def __init__(self, sesion):
        self.sesion = sesion

    def crear(self, usuario: Usuario):
        self.sesion.add(usuario)
        self.sesion.commit()
        return usuario

    def obtener_por_id(self, usuario_id: str):
        return self.sesion.query(Usuario).filter_by(id=usuario_id).first()

    def obtener_por_correo(self, correo: str):
        return self.sesion.query(Usuario).filter_by(correo=correo).first()

    def eliminar(self, usuario: Usuario):
        self.sesion.delete(usuario)
        self.sesion.commit()

    def listar(self):
        return self.sesion.query(Usuario).all()
