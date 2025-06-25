import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.tarea import Tarea, PrioridadEnum
from repositorios.tarea_repositorio import TareaRepository
from datetime import datetime

class TestTareaRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.repo = TareaRepository(self.session)

    def test_crear_tarea(self):
        tarea = Tarea(
            id="t1",
            titulo="Leer",
            descripcion="Leer un libro",
            fecha_creacion=datetime.now(),
            fecha_limite=datetime.now(),
            estado=False,
            usuario_id="u1",
            prioridad=PrioridadEnum.media
        )
        self.repo.create(tarea)
        tarea_guardada = self.repo.read("t1")
        self.assertEqual(tarea_guardada.titulo, "Leer")

    def tearDown(self):
        self.session.close()
