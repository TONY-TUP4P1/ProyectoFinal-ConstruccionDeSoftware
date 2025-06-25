import unittest
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

    def test_insertar_y_obtener_categoria(self):
        # Generar un UUID para categoria_id para insertarlo
        categoria_id_a_insertar = str(uuid.uuid4())
        nombre_categoria = "Estudios"
        
        # Llamar a la función del repositorio pasando la sesión y el ID
        categoria_repositorio.insertar_categoria(self.session, categoria_id_a_insertar, nombre_categoria)

        # Obtener todas las categorías para verificar
        categorias = categoria_repositorio.obtener_categorias(self.session)
        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0].nombre, nombre_categoria)
        self.assertEqual(categorias[0].categoria_id, categoria_id_a_insertar)

    def test_actualizar_categoria(self):
        # Primero, inserta una categoría
        categoria_id = str(uuid.uuid4())
        categoria_repositorio.insertar_categoria(self.session, categoria_id, "Deportes")
        
        # Actualiza el nombre de la categoría
        nuevo_nombre = "Actividades Físicas"
        categoria_repositorio.actualizar_categoria(self.session, categoria_id, nuevo_nombre)

        # Verifica que la categoría se haya actualizado
        categorias = categoria_repositorio.obtener_categorias(self.session) # Obtener de nuevo
        self.assertEqual(len(categorias), 1)
        self.assertEqual(categorias[0].nombre, nuevo_nombre)
        self.assertEqual(categorias[0].categoria_id, categoria_id)

    def test_eliminar_categoria(self):
        # Primero, inserta una categoría
        categoria_id = str(uuid.uuid4())
        categoria_repositorio.insertar_categoria(self.session, categoria_id, "Compras")
        
        # Elimina la categoría
        categoria_repositorio.eliminar_categoria(self.session, categoria_id)

        # Verifica que la categoría haya sido eliminada
        categorias = categoria_repositorio.obtener_categorias(self.session)
        self.assertEqual(len(categorias), 0)

