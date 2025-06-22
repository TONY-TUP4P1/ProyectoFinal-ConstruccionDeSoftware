from modelos.usuario import Usuario
from repositorios.usuario_repositorio import UsuarioRepositorio


class UsuarioServicio:
    def __init__(self, usuario_repo: UsuarioRepositorio):
        self.usuario_repo = usuario_repo

    def registrar_usuario(
            self,
            nombre,
            apellido,
            correo,
            contrasena,
            telefono=None,
            fecha_nacimiento=None):
        if self.usuario_repo.obtener_por_correo(correo):
            raise ValueError("El correo ya está registrado.")
        nuevo_usuario = Usuario(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contrasena=contrasena,
            telefono=telefono,
            fecha_nacimiento=fecha_nacimiento
        )
        return self.usuario_repo.crear(nuevo_usuario)

    def obtener_usuario(self, usuario_id: str):
        usuario = self.usuario_repo.obtener_por_id(usuario_id)
        if not usuario:
            raise ValueError("Usuario no encontrado.")
        return usuario
