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
        # Eliminar el usuario después de cada test para asegurar la limpieza
        usuario = usuario_repositorio.obtener_usuario_por_correo(self.session, getattr(self, '_last_user_email', None))
        if usuario:
            usuario_repositorio.eliminar_usuario(self.session, usuario.id)
        
        self.session.commit() # Confirmar eliminaciones
        self.session.close()
        self.engine.dispose() # Dispose of the engine to close connections
        Base.metadata.drop_all(self.engine) # Eliminar las tablas después de cada prueba
        # Añadir limpieza explícita para evitar ResourceWarning
        del self.session
        del self.engine

    def test_01_insertar_usuario(self):
        print("\n--- Ejecutando test_01_insertar_usuario (CRUD: Create) ---")
        usuario_id = str(uuid.uuid4())
        nombre_usuario = "Carlos"
        apellido_usuario = "Gómez"
        correo_usuario = "carlos@example.com"
        self._last_user_email = correo_usuario # Guardar para cleanup en tearDown
        contrasena_usuario = "secreta123"
        telefono_usuario = "999888777"
        fecha_nacimiento_usuario = date(1995, 8, 15)

        usuario_repositorio.insertar_usuario(self.session, usuario_id, nombre_usuario,
                                             apellido_usuario, correo_usuario, contrasena_usuario,
                                             telefono_usuario, fecha_nacimiento_usuario)
        self.session.commit() # Commit para que esté visible en la sesión

        usuario_guardado = usuario_repositorio.obtener_usuario_por_correo(self.session, correo_usuario)
        self.assertIsNotNone(usuario_guardado)
        self.assertEqual(usuario_guardado.id, usuario_id)
        self.assertEqual(usuario_guardado.nombre, nombre_usuario)
        self.assertEqual(usuario_guardado.correo, correo_usuario)
        self.assertEqual(usuario_guardado.fecha_nacimiento, fecha_nacimiento_usuario) # Validar fecha de nacimiento

    def test_02_obtener_usuario_por_correo(self):
        print("\n--- Ejecutando test_02_obtener_usuario_por_correo (CRUD: Read) ---")
        usuario_id = str(uuid.uuid4())
        correo_usuario = "buscar@example.com"
        self._last_user_email = correo_usuario
        usuario_repositorio.insertar_usuario(self.session, usuario_id, "Juan", "Pérez",
                                             correo_usuario, "pass123", "111222333",
                                             date(1985, 1, 1))
        self.session.commit()

        usuario_encontrado = usuario_repositorio.obtener_usuario_por_correo(self.session, correo_usuario)
        self.assertIsNotNone(usuario_encontrado)
        self.assertEqual(usuario_encontrado.correo, correo_usuario)
        self.assertEqual(usuario_encontrado.id, usuario_id)

        # Probar con un correo que no existe
        usuario_no_encontrado = usuario_repositorio.obtener_usuario_por_correo(self.session, "noexiste@example.com")
        self.assertIsNone(usuario_no_encontrado)


    def test_03_actualizar_usuario(self):
        print("\n--- Ejecutando test_03_actualizar_usuario (CRUD: Update) ---")
        usuario_id = str(uuid.uuid4())
        correo_original = "pedro@example.com"
        self._last_user_email = correo_original
        usuario_repositorio.insertar_usuario(self.session, usuario_id, "Pedro", "López",
                                             correo_original, "pass123", "111222333",
                                             date(1990, 5, 20))
        self.session.commit()

        nuevo_nombre = "Pedro Actualizado"
        nuevo_telefono = "987654321"
        usuario_repositorio.actualizar_usuario(self.session, usuario_id, nombre=nuevo_nombre, telefono=nuevo_telefono)
        self.session.commit()

        usuario_actualizado = usuario_repositorio.obtener_usuario_por_correo(self.session, correo_original)
        self.assertIsNotNone(usuario_actualizado)
        self.assertEqual(usuario_actualizado.nombre, nuevo_nombre)
        self.assertEqual(usuario_actualizado.telefono, nuevo_telefono)

    def test_04_eliminar_usuario(self):
        print("\n--- Ejecutando test_04_eliminar_usuario (CRUD: Delete) ---")
        usuario_id = str(uuid.uuid4())
        correo_eliminar = "ana@example.com"
        self._last_user_email = correo_eliminar
        usuario_repositorio.insertar_usuario(self.session, usuario_id, "Ana", "Ruiz",
                                             correo_eliminar, "anapass", "444555666",
                                             date(1988, 11, 30))
        self.session.commit()

        usuario_repositorio.eliminar_usuario(self.session, usuario_id)
        self.session.commit()

        usuario_eliminado = usuario_repositorio.obtener_usuario_por_correo(self.session, correo_eliminar)
        self.assertIsNone(usuario_eliminado)

if __name__ == '__main__':
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
