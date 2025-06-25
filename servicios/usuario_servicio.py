from sqlalchemy.orm import Session
from modelos.usuario import Usuario
from repositorios.usuario_repositorio import (
    insertar_usuario,
    obtener_usuario_por_correo,
    actualizar_usuario,
    eliminar_usuario
)

class UsuarioService:
    def __init__(self, session: Session):
        self.session = session

    def registrar_usuario(self, usuario: Usuario) -> bool:
        existente = obtener_usuario_por_correo(self.session, usuario.correo)
        if existente:
            return False
        return insertar_usuario(
            self.session, # Pasa la sesión
            usuario.id,
            usuario.nombre,
            usuario.apellido,
            usuario.correo,
            usuario.contrasena,
            usuario.telefono,
            usuario.fecha_nacimiento
        )

    def buscar_por_correo(self, correo: str):
        return obtener_usuario_por_correo(self.session, correo)

    def actualizar_usuario(self, id: str, **kwargs):
        actualizar_usuario(self.session, id, **kwargs)

    def eliminar_usuario(self, id: str):
        eliminar_usuario(self.session, id)

