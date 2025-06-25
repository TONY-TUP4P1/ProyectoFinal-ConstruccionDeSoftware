import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.categoria import Categoria
from repositorios.categoria_repositorio import CategoriaRepository

class TestCategoriaRepository(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.repo = CategoriaRepository(self.session)

    def test_crear_categoria(self):
        categoria = Categoria(
            id="c1",
            nombre="Estudios"
        )
        self.repo.create(categoria)
        categoria_guardada = self.repo.read("c1")
        self.assertEqual(categoria_guardada.nombre, "Estudios")

    def tearDown(self):
        self.session.close()
