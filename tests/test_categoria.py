import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.base import Base
from repositorios.categoria_repositorio import CategoriaRepositorio
from servicios.categoria_servicio import CategoriaServicio


class TestCategoriaServicio(unittest.TestCase):
    def setUp(self):
        # Crear una base de datos SQLite en memoria
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

        # Instanciar repositorio y servicio
        self.repo = CategoriaRepositorio(self.session)
        self.service = CategoriaServicio(self.repo)

    def tearDown(self):
        # Cerrar sesión y liberar recursos al final de cada test
        self.session.close()
        self.engine.dispose()

    def test_crear_categoria(self):
        categoria = self.service.crear_categoria("Académico")
        self.assertEqual(categoria.nombre, "Académico")

    def test_categoria_duplicada(self):
        self.service.crear_categoria("Personal")
        with self.assertRaises(ValueError):
            self.service.crear_categoria("Personal")

    def test_nombre_vacio(self):
        with self.assertRaises(ValueError):
            self.service.crear_categoria("")

if __name__ == "__main__":
    unittest.main()
