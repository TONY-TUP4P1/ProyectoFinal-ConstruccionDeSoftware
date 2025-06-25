import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.usuario import Usuario
from repositorios.usuario_repositorio import UsuarioRepository
from datetime import datetime

class TestUsuarioRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.repo = UsuarioRepository(self.session)

    def test_crear_usuario(self):
        usuario = Usuario(
            id="u1",
            nombre="Carlos",
            apellido="Gómez",
            contrasena="secreta",
            correo="carlos@example.com",
            telefono="999888777",
            fecha_nacimiento=datetime(1995, 8, 15)
        )
        self.repo.create(usuario)
        usuario_guardado = self.repo.read("u1")
        self.assertEqual(usuario_guardado.nombre, "Carlos")

    def tearDown(self):
        self.session.close()
