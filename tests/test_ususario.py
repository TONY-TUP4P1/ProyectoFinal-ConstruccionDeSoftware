import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from repositorios.usuario_repositorio import crear_usuario

class TestUsuario(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def test_crear_usuario(self):
        session = self.Session()
        usuario = crear_usuario(session, "johndoe", "johndoe@example.com")
        self.assertEqual(usuario.nombre_usuario, "johndoe")
        self.assertEqual(usuario.correo, "johndoe@example.com")