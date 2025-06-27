import unittest
import sys
import os

# Add the project root directory to sys.path
# This allows importing modules like 'data.database' or 'modelos.tarea'
# assuming the test script is in 'tests/' and the project root is the parent of 'tests/'
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base
from modelos.subtarea import Subtarea # Corrected import for Subtarea model
from modelos.tarea import Tarea, PrioridadEnum
from modelos.usuario import Usuario
from repositorios import subtarea_repositorio
from repositorios import tarea_repositorio
from repositorios import usuario_repositorio
import uuid
from datetime import datetime, date

class TestSubtareaRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine) # Create tables for the in-memory database
        Session = sessionmaker(bind=self.engine)
        self.session = Session() # Create a session for each test

        # Create a dummy parent user for the task (FK constraint)
        self.usuario_id = str(uuid.uuid4())
        dummy_usuario = Usuario(
            id=self.usuario_id,
            nombre="UsuarioSubtareaTest",
            apellido="Apellido",
            correo="subtarea@test.com",
            contrasena="pass123",
            telefono="111222333",
            fecha_nacimiento=date(1990, 1, 1)
        )
        usuario_repositorio.insertar_usuario(self.session, dummy_usuario.id,
                                            dummy_usuario.nombre, dummy_usuario.apellido,
                                            dummy_usuario.correo, dummy_usuario.contrasena,
                                            dummy_usuario.telefono, dummy_usuario.fecha_nacimiento)
        
        # Create a dummy parent task for the subtareas (FK constraint)
        self.tarea_id = str(uuid.uuid4())
        dummy_tarea = Tarea(
            tarea_id=self.tarea_id,
            titulo="Tarea Principal para Subtareas",
            descripcion="Descripción de la tarea principal de subtareas",
            fecha_creacion=datetime.now(),
            fecha_limite=date(2025, 12, 31),
            estado=False,
            prioridad=PrioridadEnum.MEDIA,
            usuario_id=self.usuario_id,
            categoria_id=None
        )
        tarea_repositorio.insertar_tarea(self.session, dummy_tarea.tarea_id,
                                         dummy_tarea.titulo, dummy_tarea.descripcion,
                                         dummy_tarea.fecha_creacion, dummy_tarea.fecha_limite,
                                         dummy_tarea.estado, dummy_tarea.prioridad,
                                         dummy_tarea.usuario_id, dummy_tarea.categoria_id)
        # Commit to ensure the user and task are in the DB before subtareas
        self.session.commit() 


    def tearDown(self):
        # Cleanup: delete everything created for each test
        # Relationships with CASCADE='all, delete-orphan' should clean subtareas when deleting the task
        # However, we explicitly delete for clarity in tests
        tarea = tarea_repositorio.obtener_tarea_por_id(self.session, self.tarea_id)
        if tarea:
            tarea_repositorio.eliminar_tarea_por_id(self.session, self.tarea_id)
        
        usuario = usuario_repositorio.obtener_usuario_por_correo(self.session, "subtarea@test.com")
        if usuario:
            usuario_repositorio.eliminar_usuario(self.session, self.usuario_id)

        self.session.commit() # Confirm deletions

        self.session.close()
        self.engine.dispose()
        # Add explicit cleanup to avoid ResourceWarning
        del self.session
        del self.engine


    def test_01_crear_subtarea(self):
        print("\n--- Ejecutando test_01_crear_subtarea (CRUD: Create) ---")
        subtarea_id = str(uuid.uuid4())
        titulo = "Paso 1 del proyecto"
        descripcion = "Hacer la investigación inicial"
        completada = False
        
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, titulo, descripcion, completada, self.tarea_id)
        self.session.commit() # Commit so it's visible in the session

        subtareas_en_db = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_en_db), 1)
        self.assertEqual(subtareas_en_db[0].subtarea_id, subtarea_id) # ✅ CORRECCIÓN: Acceder a .subtarea_id
        self.assertEqual(subtareas_en_db[0].titulo, titulo)
        self.assertEqual(subtareas_en_db[0].descripcion, descripcion)
        self.assertEqual(subtareas_en_db[0].completada, completada)
        self.assertEqual(subtareas_en_db[0].tarea_id, self.tarea_id)

    def test_02_leer_subtareas(self):
        print("\n--- Ejecutando test_02_leer_subtareas (CRUD: Read) ---")
        # Ensure there is at least one subtarea to read
        subtarea_id1 = str(uuid.uuid4())
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id1, "Subtarea para Leer 1", "", False, self.tarea_id)
        subtarea_id2 = str(uuid.uuid4())
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id2, "Subtarea para Leer 2", "", True, self.tarea_id)
        self.session.commit()

        subtareas_leidas = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_leidas), 2)
        # Verify that all subtareas associated with the task can be obtained
        self.assertIn(subtarea_id1, [s.subtarea_id for s in subtareas_leidas]) # ✅ CORRECCIÓN: Acceder a .subtarea_id
        self.assertIn(subtarea_id2, [s.subtarea_id for s in subtareas_leidas]) # ✅ CORRECCIÓN: Acceder a .subtarea_id


    def test_03_actualizar_subtarea(self):
        print("\n--- Ejecutando test_03_actualizar_subtarea (CRUD: Update) ---")
        subtarea_id = str(uuid.uuid4())
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, "Subtarea original", "Desc original", False, self.tarea_id)
        self.session.commit()

        nuevo_titulo = "Subtarea Actualizada"
        nueva_descripcion = "Descripción modificada"
        nueva_completada = True
        
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.actualizar_subtarea(self.session, subtarea_id, 
                                                titulo=nuevo_titulo, 
                                                descripcion=nueva_descripcion, 
                                                completada=nueva_completada)
        self.session.commit()

        subtareas_en_db = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_en_db), 1)
        subtarea_actualizada = subtareas_en_db[0]
        self.assertEqual(subtarea_actualizada.titulo, nuevo_titulo)
        self.assertEqual(subtarea_actualizada.descripcion, nueva_descripcion)
        self.assertEqual(subtarea_actualizada.completada, nueva_completada)


    def test_04_eliminar_subtarea(self):
        print("\n--- Ejecutando test_04_eliminar_subtarea (CRUD: Delete) ---")
        subtarea_id = str(uuid.uuid4())
        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, "Subtarea a eliminar", "", False, self.tarea_id)
        self.session.commit()

        # ✅ CORRECCIÓN: Usar subtarea_id en la llamada al repositorio
        subtarea_repositorio.eliminar_subtarea(self.session, subtarea_id)
        self.session.commit()

        subtareas_restantes = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_restantes), 0)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
