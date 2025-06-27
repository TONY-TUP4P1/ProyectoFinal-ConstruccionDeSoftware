import unittest
import sys
import os

# Añadir el directorio raíz del proyecto al sys.path
# Esto permite importar módulos como 'data.database' o 'modelos.tarea'
# asumiendo que el script de prueba está en 'tests/' y el proyecto raíz es el padre de 'tests/'
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

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
        # Añadir limpieza explícita para evitar ResourceWarning
        del self.session
        del self.engine

    def test_01_crear_etiqueta(self):
        print("\n--- Ejecutando test_01_crear_etiqueta (CRUD: Create) ---")
        # Insertar una nueva etiqueta
        etiqueta_id = str(uuid.uuid4())
        nombre_etiqueta = "Importante"
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, nombre_etiqueta)
        self.session.commit() # Commit para que esté visible en la sesión

        # Obtener la etiqueta y verificar
        etiquetas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas), 1)
        self.assertEqual(etiquetas[0].nombre, nombre_etiqueta)
        self.assertEqual(etiquetas[0].etiqueta_id, etiqueta_id)

    def test_02_leer_etiquetas(self):
        print("\n--- Ejecutando test_02_leer_etiquetas (CRUD: Read) ---")
        # Insertar algunas etiquetas para leer
        etiqueta_id1 = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id1, "EtiquetaA")
        etiqueta_id2 = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id2, "EtiquetaB")
        self.session.commit()

        etiquetas_leidas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas_leidas), 2)
        self.assertIn("EtiquetaA", [e.nombre for e in etiquetas_leidas])
        self.assertIn("EtiquetaB", [e.nombre for e in etiquetas_leidas])

    def test_03_obtener_etiqueta_por_nombre(self):
        print("\n--- Ejecutando test_03_obtener_etiqueta_por_nombre (CRUD: Read Específico) ---")
        # Insertar una etiqueta para probar
        etiqueta_id = str(uuid.uuid4())
        nombre_etiqueta = "TestNombre"
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, nombre_etiqueta)
        self.session.commit()

        # Obtener la etiqueta por nombre y verificar
        etiqueta_encontrada = etiqueta_repositorio.obtener_etiqueta_por_nombre(self.session, nombre_etiqueta)
        self.assertIsNotNone(etiqueta_encontrada)
        self.assertEqual(etiqueta_encontrada.nombre, nombre_etiqueta)
        self.assertEqual(etiqueta_encontrada.etiqueta_id, etiqueta_id)

        # Probar con un nombre que no existe
        etiqueta_no_encontrada = etiqueta_repositorio.obtener_etiqueta_por_nombre(self.session, "NoExiste")
        self.assertIsNone(etiqueta_no_encontrada)

    def test_04_actualizar_etiqueta(self):
        print("\n--- Ejecutando test_04_actualizar_etiqueta (CRUD: Update) ---")
        # Insertar una etiqueta
        etiqueta_id = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, "Urgente")
        self.session.commit()

        # Actualizar la etiqueta
        nuevo_nombre = "Crítico"
        etiqueta_repositorio.actualizar_etiqueta(self.session, etiqueta_id, nuevo_nombre)
        self.session.commit()

        # Verificar la actualización
        etiqueta_actualizada = etiqueta_repositorio.obtener_etiqueta_por_nombre(self.session, nuevo_nombre)
        self.assertIsNotNone(etiqueta_actualizada)
        self.assertEqual(etiqueta_actualizada.nombre, nuevo_nombre)
        self.assertEqual(etiqueta_actualizada.etiqueta_id, etiqueta_id)


    def test_05_eliminar_etiqueta(self):
        print("\n--- Ejecutando test_05_eliminar_etiqueta (CRUD: Delete) ---")
        # Insertar una etiqueta
        etiqueta_id = str(uuid.uuid4())
        etiqueta_repositorio.insertar_etiqueta(self.session, etiqueta_id, "General")
        self.session.commit()

        # Eliminar la etiqueta
        etiqueta_repositorio.eliminar_etiqueta(self.session, etiqueta_id)
        self.session.commit()

        # Verificar que fue eliminada
        etiquetas = etiqueta_repositorio.obtener_etiquetas(self.session)
        self.assertEqual(len(etiquetas), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
