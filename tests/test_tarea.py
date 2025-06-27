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
from modelos.tarea import Tarea, PrioridadEnum # Correcto: Importar PrioridadEnum directamente
from modelos.usuario import Usuario # Necesario para crear un usuario padre
from repositorios import tarea_repositorio # Importar el módulo de repositorio como un todo
from repositorios import usuario_repositorio # Necesario para insertar el usuario padre
from datetime import datetime, date # Import date for clearer usage
import uuid

class TestTareaRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Crear un usuario para asociar con las tareas (FK constraint)
        self.usuario_id = str(uuid.uuid4())
        dummy_usuario = Usuario(
            id=self.usuario_id,
            nombre="Usuario",
            apellido="Prueba",
            correo="usuario@prueba.com",
            contrasena="password123",
            telefono="123456789",
            fecha_nacimiento=date(2000, 1, 1) # Usar date.date()
        )
        usuario_repositorio.insertar_usuario(self.session, dummy_usuario.id,
                                            dummy_usuario.nombre, dummy_usuario.apellido,
                                            dummy_usuario.correo, dummy_usuario.contrasena,
                                            dummy_usuario.telefono, dummy_usuario.fecha_nacimiento)
        self.session.commit() # Confirmar que el usuario se ha insertado


    def tearDown(self):
        # Limpieza: Eliminar la tarea y el usuario después de cada test
        tarea = tarea_repositorio.obtener_tarea_por_id(self.session, getattr(self, '_last_tarea_id', None))
        if tarea:
            tarea_repositorio.eliminar_tarea_por_id(self.session, tarea.tarea_id)

        usuario = usuario_repositorio.obtener_usuario_por_correo(self.session, "usuario@prueba.com")
        if usuario:
            usuario_repositorio.eliminar_usuario(self.session, usuario.id)

        self.session.commit() # Confirmar eliminaciones
        self.session.close()
        self.engine.dispose()
        # Añadir limpieza explícita para evitar ResourceWarning
        del self.session
        del self.engine


    def test_01_crear_tarea(self):
        print("\n--- Ejecutando test_01_crear_tarea (CRUD: Create) ---")
        tarea_id = str(uuid.uuid4())
        self._last_tarea_id = tarea_id # Guardar para cleanup en tearDown
        titulo_tarea = "Leer un libro"
        descripcion_tarea = "Capítulo 5 de Clean Code"
        fecha_limite = date(2025, 12, 31) # Usar date object
        estado = False
        prioridad = PrioridadEnum.MEDIA # Pasar el objeto Enum

        tarea_repositorio.insertar_tarea(self.session, tarea_id, titulo_tarea, descripcion_tarea,
                                         datetime.now(), fecha_limite, estado, prioridad,
                                         self.usuario_id, None)
        self.session.commit() # Commit para que esté visible en la sesión

        tarea_guardada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertIsNotNone(tarea_guardada)
        self.assertEqual(tarea_guardada.titulo, titulo_tarea)
        self.assertEqual(tarea_guardada.estado, estado)
        self.assertEqual(tarea_guardada.prioridad, prioridad)
        self.assertEqual(tarea_guardada.usuario_id, self.usuario_id)
        self.assertEqual(tarea_guardada.fecha_limite.date(), fecha_limite)


    def test_02_leer_tareas_por_usuario(self):
        print("\n--- Ejecutando test_02_leer_tareas_por_usuario (CRUD: Read) ---")
        # Insertar tareas para el usuario ficticio
        tarea_id1 = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id1, "Tarea de Prueba 1", "Desc 1",
                                         datetime.now(), date(2025, 7, 1), False, PrioridadEnum.ALTA,
                                         self.usuario_id, None)
        tarea_id2 = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id2, "Tarea de Prueba 2", "Desc 2",
                                         datetime.now(), date(2025, 7, 2), True, PrioridadEnum.BAJA,
                                         self.usuario_id, None)
        self.session.commit()

        tareas_usuario = tarea_repositorio.obtener_tareas_por_usuario(self.session, self.usuario_id)
        self.assertEqual(len(tareas_usuario), 2)
        self.assertIn(tarea_id1, [t.tarea_id for t in tareas_usuario])
        self.assertIn(tarea_id2, [t.tarea_id for t in tareas_usuario])

        # Probar filtro por estado
        tareas_pendientes = tarea_repositorio.obtener_tareas_por_usuario(self.session, self.usuario_id, estado=False)
        self.assertEqual(len(tareas_pendientes), 1)
        self.assertEqual(tareas_pendientes[0].tarea_id, tarea_id1)

        tareas_completadas = tarea_repositorio.obtener_tareas_por_usuario(self.session, self.usuario_id, estado=True)
        self.assertEqual(len(tareas_completadas), 1)
        self.assertEqual(tareas_completadas[0].tarea_id, tarea_id2)


    def test_03_actualizar_tarea(self):
        print("\n--- Ejecutando test_03_actualizar_tarea (CRUD: Update) ---")
        tarea_id = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id, "Tarea Original", "Desc Original",
                                         datetime.now(), date(2025,1,1), False, PrioridadEnum.MEDIA,
                                         self.usuario_id, None)
        self.session.commit()

        nueva_fecha_limite = date(2025, 12, 31)
        tarea_repositorio.actualizar_tarea(self.session, tarea_id,
                                           titulo="Tarea Actualizada",
                                           descripcion="Descripción Modificada",
                                           fecha_limite=nueva_fecha_limite,
                                           estado=True,
                                           prioridad=PrioridadEnum.ALTA,
                                           categoria_id=None)
        self.session.commit()

        tarea_actualizada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertEqual(tarea_actualizada.titulo, "Tarea Actualizada")
        self.assertEqual(tarea_actualizada.descripcion, "Descripción Modificada")
        self.assertEqual(tarea_actualizada.fecha_limite.date(), nueva_fecha_limite)
        self.assertEqual(tarea_actualizada.estado, True)
        self.assertEqual(tarea_actualizada.prioridad, PrioridadEnum.ALTA)
        self.assertEqual(tarea_actualizada.usuario_id, self.usuario_id)


    def test_04_eliminar_tarea(self):
        print("\n--- Ejecutando test_04_eliminar_tarea (CRUD: Delete) ---")
        tarea_id = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id, "Tarea a Eliminar", "",
                                         datetime.now(), date(2025, 7, 10), False, PrioridadEnum.BAJA,
                                         self.usuario_id, None)
        self.session.commit()

        tarea_repositorio.eliminar_tarea_por_id(self.session, tarea_id)
        self.session.commit()

        tarea_eliminada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertIsNone(tarea_eliminada)


if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
