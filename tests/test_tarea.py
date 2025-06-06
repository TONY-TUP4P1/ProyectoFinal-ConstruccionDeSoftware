import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base
from repositorios.tarea_repositorio import crear_tarea
from repositorios.usuario_repositorio import crear_usuario

class TestTarea(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def test_crear_tarea(self):
        session = self.Session()
        usuario = crear_usuario(session, "johndoe", "johndoe@example.com")
        tarea = crear_tarea(session, "Tarea 1", "Descripción de la tarea", usuario.id)
        self.assertEqual(tarea.nombre, "Tarea 1")
        self.assertEqual(tarea.descripcion, "Descripción de la tarea")
