import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base # Importar Base desde data.database
from modelos.tarea import Tarea, PrioridadEnum
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


    def tearDown(self):
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine)

    def test_insertar_y_obtener_tarea(self):
        tarea_id = str(uuid.uuid4())
        titulo_tarea = "Leer un libro"
        descripcion_tarea = "Capítulo 5 de Clean Code"
        fecha_limite = date(2025, 12, 31) # Usar date object
        estado = False
        prioridad = PrioridadEnum.MEDIA.value # Acceder al valor de la enumeración

        tarea_repositorio.insertar_tarea(self.session, tarea_id, titulo_tarea, descripcion_tarea,
                                         datetime.now(), fecha_limite, estado, prioridad,
                                         self.usuario_id, None) # No hay categoria_id por ahora

        tarea_guardada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertIsNotNone(tarea_guardada)
        self.assertEqual(tarea_guardada.titulo, titulo_tarea)
        self.assertEqual(tarea_guardada.estado, estado)
        self.assertEqual(tarea_guardada.prioridad, prioridad) # Ya compara el valor de la cadena
        self.assertEqual(tarea_guardada.usuario_id, self.usuario_id)
        # Asegurarse de que fecha_limite se guarda como date
        self.assertEqual(tarea_guardada.fecha_limite, fecha_limite)


    def test_obtener_tareas_por_usuario(self):
        tarea_id1 = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id1, "Tarea 1 del usuario", "",
                                         datetime.now(), date(2025, 7, 1), False, PrioridadEnum.ALTA.value,
                                         self.usuario_id, None)

        tarea_id2 = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id2, "Tarea 2 del usuario", "",
                                         datetime.now(), date(2025, 7, 2), True, PrioridadEnum.BAJA.value,
                                         self.usuario_id, None)

        tareas_usuario = tarea_repositorio.obtener_tareas_por_usuario(self.session, self.usuario_id)
        self.assertEqual(len(tareas_usuario), 2)
        # Filtrar por estado (ejemplo para el nuevo parámetro en servicio)
        tareas_pendientes = tarea_repositorio.obtener_tareas_por_usuario(self.session, self.usuario_id, estado=False)
        self.assertEqual(len(tareas_pendientes), 1)
        self.assertEqual(tareas_pendientes[0].tarea_id, tarea_id1)

    def test_actualizar_tarea(self):
        tarea_id = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id, "Tarea Vieja", "Descripción Vieja",
                                         datetime.now(), date(2025,1,1), False, PrioridadEnum.MEDIA.value,
                                         self.usuario_id, None)

        nueva_fecha_limite = date(2025, 12, 31) # Usar date object
        tarea_repositorio.actualizar_tarea(self.session, tarea_id,
                                           titulo="Tarea Nueva",
                                           descripcion="Descripción Nueva",
                                           fecha_limite=nueva_fecha_limite,
                                           estado=True,
                                           prioridad=PrioridadEnum.ALTA.value, # Usar el valor de la enumeración
                                           categoria_id=None)

        tarea_actualizada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertEqual(tarea_actualizada.titulo, "Tarea Nueva")
        self.assertEqual(tarea_actualizada.descripcion, "Descripción Nueva")
        self.assertEqual(tarea_actualizada.fecha_limite, nueva_fecha_limite) # Ahora debe coincidir correctamente
        self.assertEqual(tarea_actualizada.estado, True)
        self.assertEqual(tarea_actualizada.prioridad, PrioridadEnum.ALTA.value) # Ya compara el valor de la cadena


    def test_eliminar_tarea_por_id(self):
        tarea_id = str(uuid.uuid4())
        tarea_repositorio.insertar_tarea(self.session, tarea_id, "Tarea a Eliminar", "",
                                         datetime.now(), date(2025, 7, 10), False, PrioridadEnum.BAJA.value,
                                         self.usuario_id, None)

        tarea_repositorio.eliminar_tarea_por_id(self.session, tarea_id)

        tarea_eliminada = tarea_repositorio.obtener_tarea_por_id(self.session, tarea_id)
        self.assertIsNone(tarea_eliminada)

