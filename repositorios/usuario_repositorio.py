from sqlalchemy.orm import Session
from modelos.usuario import Usuario

class UsuarioRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, usuario: Usuario):
        self.session.add(usuario)
        self.session.commit()

    def read(self, usuario_id: str):
        return self.session.query(Usuario).filter_by(id=usuario_id).first()

    def update(self, usuario: Usuario):
        self.session.commit()

    def delete(self, usuario_id: str):
        usuario = self.read(usuario_id)
        if usuario:
            self.session.delete(usuario)
            self.session.commit()
