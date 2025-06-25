import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.subtarea import SubTarea
from repositorios.subtarea_repositorio import SubTareaRepository

class TestSubTareaRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.repo = SubTareaRepository(self.session)

    def test_crear_subtarea(self):
        subtarea = SubTarea(
            id="s1",
            titulo="Paso 1",
            descripcion="Hacer algo",
            completada=False,
            tarea_id="t1"
        )
        self.repo.create(subtarea)
        subtarea_guardada = self.repo.read("s1")
        self.assertEqual(subtarea_guardada.titulo, "Paso 1")

    def tearDown(self):
        self.session.close()
