import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.base import Base
from repositorios.etiqueta_repositorio import EtiquetaRepositorio
from servicios.etiqueta_servicio import EtiquetaServicio


class TestEtiquetaServicio(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        self.repo = EtiquetaRepositorio(self.session)
        self.service = EtiquetaServicio(self.repo)

    def tearDown(self):
        self.session.close()
        self.engine.dispose()

    def test_crear_etiqueta(self):
        etiqueta = self.service.crear_etiqueta("Importante")
        self.assertEqual(etiqueta.nombre, "Importante")

    def test_etiqueta_duplicada(self):
        self.service.crear_etiqueta("Trabajo")
        with self.assertRaises(ValueError):
            self.service.crear_etiqueta("Trabajo")

    def test_etiqueta_vacia(self):
        with self.assertRaises(ValueError):
            self.service.crear_etiqueta("")

if __name__ == "__main__":
    unittest.main()
