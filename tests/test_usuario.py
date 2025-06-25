import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data.database import Base # Importar Base desde data.database
from modelos.usuario import Usuario
from repositorios import usuario_repositorio # Importar el módulo de repositorio como un todo
from datetime import datetime, date # Import date for clearer usage
import uuid

class TestUsuarioRepository(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine) # Crear las tablas
        Session = sessionmaker(bind=self.engine)
        self.session = Session()

    def tearDown(self):
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine) # Eliminar las tablas después de cada prueba

    def test_insertar_y_obtener_usuario(self):
        usuario_id = str(uuid.uuid4())
        nombre_usuario = "Carlos"
        apellido_usuario = "Gómez"
        correo_usuario = "carlos@example.com"
        contrasena_usuario = "secreta123"
        telefono_usuario = "999888777"
        fecha_nacimiento_usuario = date(1995, 8, 15) # Use date.date() instead of datetime.datetime().date()

        usuario_repositorio.insertar_usuario(self.session, usuario_id, nombre_usuario,
                                             apellido_usuario, correo_usuario, contrasena_usuario,
                                             telefono_usuario, fecha_nacimiento_usuario)

        usuario_guardado = usuario_repositorio.obtener_usuario_por_correo(self.session, correo_usuario)
        self.assertIsNotNone(usuario_guardado)
        self.assertEqual(usuario_guardado.id, usuario_id)
        self.assertEqual(usuario_guardado.nombre, nombre_usuario)
        self.assertEqual(usuario_guardado.correo, correo_usuario)

    def test_actualizar_usuario(self):
        usuario_id = str(uuid.uuid4())
        usuario_repositorio.insertar_usuario(self.session, usuario_id, "Pedro", "López",
                                             "pedro@example.com", "pass123", "111222333",
                                             date(1990, 5, 20)) # Use date.date()

        nuevo_nombre = "Pedro Actualizado"
        nuevo_telefono = "987654321"
        usuario_repositorio.actualizar_usuario(self.session, usuario_id, nombre=nuevo_nombre, telefono=nuevo_telefono)

        usuario_actualizado = usuario_repositorio.obtener_usuario_por_correo(self.session, "pedro@example.com")
        self.assertIsNotNone(usuario_actualizado)
        self.assertEqual(usuario_actualizado.nombre, nuevo_nombre)
        self.assertEqual(usuario_actualizado.telefono, nuevo_telefono)

    def test_eliminar_usuario(self):
        usuario_id = str(uuid.uuid4())
        usuario_repositorio.insertar_usuario(self.session, usuario_id, "Ana", "Ruiz",
                                             "ana@example.com", "anapass", "444555666",
                                             date(1988, 11, 30)) # Use date.date()

        usuario_repositorio.eliminar_usuario(self.session, usuario_id)

        usuario_eliminado = usuario_repositorio.obtener_usuario_por_correo(self.session, "ana@example.com")
        self.assertIsNone(usuario_eliminado)

