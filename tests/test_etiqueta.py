import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.etiqueta import Etiqueta
from repositorios.etiqueta_repositorio import EtiquetaRepository

class TestEtiquetaRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.repo = EtiquetaRepository(self.session)

    def test_crear_etiqueta(self):
        etiqueta = Etiqueta(
            id="e1",
            nombre="Importante",
            tarea_id="t1"
        )
        self.repo.create(etiqueta)
        etiqueta_guardada = self.repo.read("e1")
        self.assertEqual(etiqueta_guardada.nombre, "Importante")

    def tearDown(self):
        self.session.close()
