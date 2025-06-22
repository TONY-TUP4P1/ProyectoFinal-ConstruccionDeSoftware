import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.base import Base
from modelos.usuario import Usuario
from repositorios.usuario_repositorio import UsuarioRepositorio
from servicios.usuario_servicio import UsuarioServicio


class TestUsuarioServicio(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        repo = UsuarioRepositorio(self.session)
        self.service = UsuarioServicio(repo)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_registro_exitoso(self):
        usuario = self.service.registrar_usuario(
            nombre="Antony",
            apellido="Munive",
            correo="72310206@continental.edu.pe",
            contrasena="72310206"
        )
        self.assertEqual(usuario.correo, "72310206@continental.edu.pe")

    def test_correo_duplicado(self):
        self.service.registrar_usuario("Test", "Uno", "repite@example.com", "clave123")
        with self.assertRaises(ValueError):
            self.service.registrar_usuario("Test", "Dos", "repite@example.com", "clave123")

if __name__ == '__main__':
    unittest.main()
