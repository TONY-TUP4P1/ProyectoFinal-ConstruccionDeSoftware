import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base # Importar Base desde data.database
from modelos.etiqueta import Etiqueta
from repositorios import etiqueta_repositorio # Importar el módulo de repositorio como un todo
import uuid

class TestEtiquetaRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine)

    def test_insertar_y_obtener_etiqueta(self):
        # Insertar una nueva etiqueta
        etiqueta_id = str(uuid.uuid4())
        nombre_etiqueta = "Importante"
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, nombre_etiqueta)

        # Obtener la etiqueta y verificar
        etiquetas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas), 1)
        self.assertEqual(etiquetas[0].nombre, nombre_etiqueta)
        self.assertEqual(etiquetas[0].etiqueta_id, etiqueta_id)

    def test_actualizar_etiqueta(self):
        # Insertar una etiqueta
        etiqueta_id = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, "Urgente")

        # Actualizar la etiqueta
        nuevo_nombre = "Crítico"
        etiqueta_repositorio.actualizar_etiqueta(self.session, etiqueta_id, nuevo_nombre)

        # Verificar la actualización
        etiquetas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas), 1)
        self.assertEqual(etiquetas[0].nombre, nuevo_nombre)
        self.assertEqual(etiquetas[0].etiqueta_id, etiqueta_id)


    def test_eliminar_etiqueta(self):
        # Insertar una etiqueta
        etiqueta_id = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, "General")

        # Eliminar la etiqueta
        etiqueta_repositorio.eliminar_etiqueta(self.session, etiqueta_id)

        # Verificar que fue eliminada
        etiquetas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas), 0)

