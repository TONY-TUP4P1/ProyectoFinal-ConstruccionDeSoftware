import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base # Importar Base desde data.database
from modelos.subtarea import Subtarea # Corregido a Subtarea
from modelos.tarea import Tarea, PrioridadEnum # Necesario para crear una tarea padre
from modelos.usuario import Usuario # Necesario para crear un usuario padre para la tarea
from repositorios import subtarea_repositorio # Importar el módulo
from repositorios import tarea_repositorio # Necesario para insertar la tarea padre
from repositorios import usuario_repositorio # Necesario para insertar el usuario padre
import uuid
from datetime import datetime, date

class TestSubtareaRepository(unittest.TestCase): # Corregido a TestSubtareaRepository
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

        # Crear un usuario padre para la tarea (FK constraint)
        self.usuario_id = str(uuid.uuid4())
        dummy_usuario = Usuario(
            id=self.usuario_id,
            nombre="UsuarioSub",
            apellido="Prueba",
            correo="sub@prueba.com",
            contrasena="passsub",
            telefono="111222333",
            fecha_nacimiento=date(1990, 1, 1)
        )
        usuario_repositorio.insertar_usuario(self.session, dummy_usuario.id,
                                            dummy_usuario.nombre, dummy_usuario.apellido,
                                            dummy_usuario.correo, dummy_usuario.contrasena,
                                            dummy_usuario.telefono, dummy_usuario.fecha_nacimiento)

        # Crear una tarea padre para las subtareas (FK constraint)
        self.tarea_id = str(uuid.uuid4())
        dummy_tarea = Tarea(
            tarea_id=self.tarea_id,
            titulo="Tarea Principal de Subtarea",
            descripcion="Descripción de la tarea principal de subtarea",
            fecha_creacion=datetime.now(),
            fecha_limite=date(2025, 12, 31), # Usar date object
            estado=False,
            prioridad=PrioridadEnum.MEDIA.value,
            usuario_id=self.usuario_id, # Usar el ID del usuario ficticio
            categoria_id=None
        )
        # Asumo que tu insertar_tarea del repositorio devuelve el objeto Tarea
        tarea_repositorio.insertar_tarea(self.session, dummy_tarea.tarea_id,
                                         dummy_tarea.titulo, dummy_tarea.descripcion,
                                         dummy_tarea.fecha_creacion, dummy_tarea.fecha_limite,
                                         dummy_tarea.estado, dummy_tarea.prioridad,
                                         dummy_tarea.usuario_id, dummy_tarea.categoria_id)

    def tearDown(self):
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine)

    def test_insertar_y_obtener_subtarea(self):
        subtarea_id = str(uuid.uuid4())
        titulo_subtarea = "Paso 1: Hacer algo"
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, titulo_subtarea, "Descripción del paso 1", False, self.tarea_id)

        subtareas_de_tarea = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_de_tarea), 1)
        self.assertEqual(subtareas_de_tarea[0].titulo, titulo_subtarea)
        self.assertEqual(subtareas_de_tarea[0].completada, False)
        self.assertEqual(subtareas_de_tarea[0].tarea_id, self.tarea_id)

    def test_actualizar_subtarea(self):
        subtarea_id = str(uuid.uuid4())
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, "Paso a actualizar", None, False, self.tarea_id)

        nuevo_titulo = "Paso Actualizado"
        nueva_completada = True
        subtarea_repositorio.actualizar_subtarea(self.session, subtarea_id, titulo=nuevo_titulo, completada=nueva_completada)

        subtareas_de_tarea = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_de_tarea), 1)
        self.assertEqual(subtareas_de_tarea[0].titulo, nuevo_titulo)
        self.assertEqual(subtareas_de_tarea[0].completada, nueva_completada)

    def test_eliminar_subtarea(self):
        subtarea_id = str(uuid.uuid4())
        subtarea_repositorio.insertar_subtarea(self.session, subtarea_id, "Paso a eliminar", None, False, self.tarea_id)

        subtarea_repositorio.eliminar_subtarea(self.session, subtarea_id)

        subtareas_restantes = subtarea_repositorio.obtener_subtareas_por_tarea(self.session, self.tarea_id)
        self.assertEqual(len(subtareas_restantes), 0)

