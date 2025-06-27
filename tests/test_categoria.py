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
from modelos.categoria import Categoria
from repositorios import categoria_repositorio # Importar el módulo de repositorio como un todo
import uuid # Necesario para generar IDs

class TestCategoriaRepository(unittest.TestCase):
    def setUp(self):
        # Usar una base de datos SQLite en memoria para pruebas aisladas
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine) # Crear tablas para la base de datos en memoria
        Session = sessionmaker(bind=self.engine)
        self.session = Session() # Crear una sesión para cada prueba

    def tearDown(self):
        # Cerrar la sesión y liberar el motor (cerrar conexiones)
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine) # Eliminar las tablas después de cada prueba
        # Añadir limpieza explícita para evitar ResourceWarning
        del self.session
        del self.engine

    def test_01_insertar_categoria(self):
        print("\n--- Ejecutando test_01_insertar_categoria (CRUD: Create) ---")
        # Generar un UUID para categoria_id para insertarlo (este ID no se pasa a insertar_categoria directamente)
        nombre_categoria = "Estudios"
        
        # Llamar a la función del repositorio pasando solo la sesión y el nombre
        # La función insertar_categoria en el repositorio se encarga de crear el ID
        categoria_id_insertada = categoria_repositorio.insertar_categoria(self.session, nombre_categoria)
        self.session.commit() # Commit para que esté visible en la sesión

        # Obtener todas las categorías para verificar
        categorias = categoria_repositorio.obtener_categorias(self.session)
        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0].nombre, nombre_categoria)
        self.assertEqual(categorias[0].categoria_id, categoria_id_insertada) # Ahora comparamos con el ID devuelto


    def test_02_obtener_categorias(self):
        print("\n--- Ejecutando test_02_obtener_categorias (CRUD: Read) ---")
        # Insertar algunas categorías para leer
        # No pasar el ID aquí, la función insertar_categoria lo maneja
        categoria_id1 = categoria_repositorio.insertar_categoria(self.session, "Trabajo")
        categoria_id2 = categoria_repositorio.insertar_categoria(self.session, "Personal")
        self.session.commit()

        categorias = categoria_repositorio.obtener_categorias(self.session)
        self.assertEqual(len(categorias), 2)
        self.assertIn("Trabajo", [c.nombre for c in categorias])
        self.assertIn("Personal", [c.nombre for c in categorias])


    def test_03_actualizar_categoria(self):
        print("\n--- Ejecutando test_03_actualizar_categoria (CRUD: Update) ---")
        # Primero, inserta una categoría y captura su ID
        categoria_id = categoria_repositorio.insertar_categoria(self.session, "Deportes")
        self.session.commit()
        
        # Actualiza el nombre de la categoría
        nuevo_nombre = "Actividades Físicas"
        categoria_repositorio.actualizar_categoria(self.session, categoria_id, nuevo_nombre)
        self.session.commit()

        # Verifica que la categoría se haya actualizado
        categorias = categoria_repositorio.obtener_categorias(self.session) # Obtener de nuevo
        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0].nombre, nuevo_nombre)
        self.assertEqual(categorias[0].categoria_id, categoria_id)

    def test_04_eliminar_categoria(self):
        print("\n--- Ejecutando test_04_eliminar_categoria (CRUD: Delete) ---")
        # Primero, inserta una categoría y captura su ID
        categoria_id = categoria_repositorio.insertar_categoria(self.session, "Compras")
        self.session.commit()
        
        # Elimina la categoría
        categoria_repositorio.eliminar_categoria(self.session, categoria_id)
        self.session.commit()

        # Verifica que la categoría haya sido eliminada
        categorias = categoria_repositorio.obtener_categorias(self.session)
        self.assertEqual(len(categorias), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
