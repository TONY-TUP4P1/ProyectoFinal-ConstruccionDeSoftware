from sqlalchemy.orm import Session
from modelos.usuario import Usuario
from repositorios.usuario_repositorio import UsuarioRepository

class UsuarioService:
    def __init__(self, session: Session):
        self.repo = UsuarioRepository(session)

    def registrar(self, usuario: Usuario):
        self.repo.create(usuario)

    def obtener_usuario(self, usuario_id: str):
        return self.repo.read(usuario_id)

    def eliminar_usuario(self, usuario_id: str):
        self.repo.delete(usuario_id)
