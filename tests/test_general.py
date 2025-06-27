import unittest
import sys
import os
import uuid
from datetime import datetime, date

# Añadir el directorio raíz del proyecto al sys.path
script_dir = os.path.dirname(__file__)
project_root = os.path.abspath(os.path.join(script_dir, os.pardir))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Importar módulos de la base de datos, modelos y servicios
from data.database import SessionLocal, Base, engine, crear_tablas
from modelos.usuario import Usuario
from modelos.tarea import Tarea, PrioridadEnum
from modelos.subtarea import Subtarea
from modelos.etiqueta import Etiqueta
from modelos.categoria import Categoria # Aunque no se usa directamente en este test, es bueno tenerla si es parte del esquema
from servicios.usuario_servicio import UsuarioService
from servicios.tarea_servicio import TareaService
from servicios.etiqueta_servicio import EtiquetaService
from servicios.categoria_servicio import CategoriaService

class TestGeneralApplicationFlow(unittest.TestCase):
    """
    Clase para realizar pruebas de integración que cubren el flujo completo
    de la aplicación: registro, login y gestión de tareas con subtareas y etiquetas.
    """

    @classmethod
    def setUpClass(cls):
        """
        Configuración inicial para todas las pruebas en esta clase.
        Crea las tablas en una base de datos en memoria.
        """
        print("\n--- Configurando la base de datos en memoria para TestGeneralApplicationFlow ---")
        Base.metadata.create_all(engine) # Asegura que todas las tablas existan
        print("--- Tablas creadas en la base de datos en memoria ---")

    @classmethod
    def tearDownClass(cls):
        """
        Limpieza final después de que todas las pruebas de la clase han terminado.
        Elimina todas las tablas de la base de datos en memoria.
        """
        print("\n--- Limpiando la base de datos en memoria después de TestGeneralApplicationFlow ---")
        Base.metadata.drop_all(engine)
        engine.dispose() # Cierra las conexiones del motor
        print("--- Tablas eliminadas y motor de DB dispuesto ---")


    def setUp(self):
        """
        Configuración antes de cada prueba individual.
        Abre una nueva sesión de base de datos para cada test y reinicia los servicios.
        """
        self.session = SessionLocal()
        self.usuario_service = UsuarioService(self.session)
        self.tarea_service = TareaService(self.session)
        self.etiqueta_service = EtiquetaService(self.session)
        self.categoria_service = CategoriaService(self.session) # Inicializa el servicio de categoría

    def tearDown(self):
        """
        Limpieza después de cada prueba individual.
        Hace rollback de la sesión para asegurar que los cambios no persistan
        entre tests, y cierra la sesión.
        """
        self.session.rollback() # Deshace cualquier cambio hecho en la prueba actual
        self.session.close()

    def test_01_user_registration_and_login_flow(self):
        """
        Prueba el flujo de registro y login de un usuario.
        """
        print("\n--- Ejecutando test_01_user_registration_and_login_flow ---")
        user_id = str(uuid.uuid4())
        email = "testuser@example.com"
        password = "Password123"
        dob = date(1990, 1, 1)

        # 1. Registrar usuario
        print(f"Registrando usuario: {email}")
        new_user = Usuario(id=user_id, nombre="Test", apellido="User", correo=email,
                           contrasena=password, telefono="123456789", fecha_nacimiento=dob)
        registered = self.usuario_service.registrar_usuario(new_user)
        self.assertTrue(registered, "Debería ser posible registrar un nuevo usuario.")
        self.session.commit() # Commit para que el usuario sea visible para la siguiente operación

        # 2. Intentar registrar el mismo usuario (debería fallar)
        print(f"Intentando registrar usuario existente: {email}")
        registered_again = self.usuario_service.registrar_usuario(new_user)
        self.assertFalse(registered_again, "No debería ser posible registrar un usuario con un correo existente.")
        self.session.rollback() # Deshacer el intento de registro fallido

        # 3. Iniciar sesión con el usuario
        print(f"Iniciando sesión con usuario: {email}")
        logged_in_user = self.usuario_service.buscar_por_correo(email)
        self.assertIsNotNone(logged_in_user, "El usuario debería existir en la base de datos.")
        self.assertEqual(logged_in_user.correo, email, "El correo del usuario logueado debe coincidir.")
        self.assertEqual(logged_in_user.contrasena, password, "La contraseña del usuario logueado debe coincidir.")
        print(f"Usuario {email} registrado y logueado con éxito.")

    def test_02_task_crud_with_subtasks_and_tags_flow(self):
        """
        Prueba el flujo CRUD de tareas, incluyendo subtareas y etiquetas.
        """
        print("\n--- Ejecutando test_02_task_crud_with_subtasks_and_tags_flow ---")
        # Preparación: Crear y loguear un usuario para la tarea
        user_id = str(uuid.uuid4())
        email = "taskuser@example.com"
        password = "TaskPass123"
        dob = date(1995, 5, 5)
        new_user = Usuario(id=user_id, nombre="Task", apellido="User", correo=email,
                           contrasena=password, telefono="987654321", fecha_nacimiento=dob)
        self.usuario_service.registrar_usuario(new_user)
        self.session.commit() # Commit del usuario

        # 1. Crear una tarea con subtareas y etiquetas
        print("Creando una nueva tarea con subtareas y etiquetas...")
        tarea_id = str(uuid.uuid4())
        titulo = "Completar Proyecto Final"
        descripcion = "Desarrollar la interfaz de usuario y conectar la base de datos."
        fecha_limite = date(2025, 7, 30)
        estado = False
        prioridad = PrioridadEnum.ALTA
        etiquetas_str = "Urgente, Universidad"
        subtareas_data = [
            {"titulo": "Diseñar UI", "completada": False},
            {"titulo": "Implementar lógica de negocio", "completada": False}
        ]

        nueva_tarea = Tarea(
            tarea_id=tarea_id,
            usuario_id=user_id,
            titulo=titulo,
            descripcion=descripcion,
            fecha_creacion=datetime.now(),
            fecha_limite=fecha_limite,
            estado=estado,
            prioridad=prioridad,
            categoria_id=None # No estamos probando categorías en este flujo
        )
        created = self.tarea_service.crear_tarea(nueva_tarea, subtareas_data, etiquetas_str)
        self.assertTrue(created, "La tarea debería ser creada exitosamente.")
        self.session.commit() # Commit explícito para asegurar que todo esté en la DB

        # Verificar la tarea creada
        tarea_db = self.tarea_service.obtener_por_id(tarea_id)
        self.assertIsNotNone(tarea_db, "La tarea debería existir en la base de datos.")
        self.assertEqual(tarea_db.titulo, titulo)
        self.assertEqual(len(tarea_db.subtareas), 2, "Debería haber 2 subtareas.")
        self.assertEqual(len(tarea_db.etiquetas), 2, "Debería haber 2 etiquetas asociadas.")
        etiquetas_nombres = {e.nombre for e in tarea_db.etiquetas}
        self.assertIn("Urgente", etiquetas_nombres)
        self.assertIn("Universidad", etiquetas_nombres)
        print(f"Tarea '{titulo}' creada y verificada.")

        # 2. Actualizar la tarea
        print("Actualizando la tarea...")
        updated_titulo = "Finalizar Proyecto de Desarrollo"
        updated_descripcion = "Refactorizar código y preparar demo."
        updated_estado = True
        updated_prioridad = PrioridadEnum.MEDIA
        updated_etiquetas_str = "Finalizado, Importante"
        updated_subtareas_data = [
            {"titulo": "Diseñar UI", "completada": True}, # Completar una subtarea
            {"titulo": "Implementar lógica de negocio", "completada": False},
            {"titulo": "Preparar presentación", "completada": False} # Añadir una nueva subtarea
        ]

        datos_a_actualizar = {
            "titulo": updated_titulo,
            "descripcion": updated_descripcion,
            "estado": updated_estado,
            "prioridad": updated_prioridad,
        }
        updated = self.tarea_service.actualizar_tarea_con_subtareas(tarea_id, datos_a_actualizar, updated_subtareas_data, updated_etiquetas_str)
        self.assertTrue(updated, "La tarea debería ser actualizada exitosamente.")
        self.session.commit() # Commit explícito para asegurar que todo esté en la DB

        # Verificar la tarea actualizada
        tarea_db_updated = self.tarea_service.obtener_por_id(tarea_id)
        self.assertIsNotNone(tarea_db_updated)
        self.assertEqual(tarea_db_updated.titulo, updated_titulo)
        self.assertEqual(tarea_db_updated.estado, updated_estado)
        self.assertEqual(len(tarea_db_updated.subtareas), 3, "Debería haber 3 subtareas después de la actualización.")
        subtarea_titulos_updated = {s.titulo for s in tarea_db_updated.subtareas}
        self.assertIn("Diseñar UI", subtarea_titulos_updated)
        self.assertIn("Preparar presentación", subtarea_titulos_updated)
        self.assertIn("Implementar lógica de negocio", subtarea_titulos_updated)
        
        # Verificar que la subtarea "Diseñar UI" está completada
        ui_subtarea = next((s for s in tarea_db_updated.subtareas if s.titulo == "Diseñar UI"), None)
        self.assertIsNotNone(ui_subtarea)
        self.assertTrue(ui_subtarea.completada, "La subtarea 'Diseñar UI' debería estar completada.")

        # Verificar etiquetas actualizadas
        etiquetas_nombres_updated = {e.nombre for e in tarea_db_updated.etiquetas}
        self.assertEqual(len(etiquetas_nombres_updated), 2, "Debería haber 2 etiquetas actualizadas.")
        self.assertIn("Finalizado", etiquetas_nombres_updated)
        self.assertIn("Importante", etiquetas_nombres_updated)
        self.assertNotIn("Urgente", etiquetas_nombres_updated) # La antigua etiqueta debe haberse removido
        print(f"Tarea '{updated_titulo}' actualizada y verificada.")

        # 3. Eliminar la tarea
        print("Eliminando la tarea...")
        deleted = self.tarea_service.eliminar_tarea(tarea_id)
        self.assertTrue(deleted, "La tarea debería ser eliminada exitosamente.")
        self.session.commit() # Commit explícito

        # Verificar que la tarea no existe
        tarea_db_deleted = self.tarea_service.obtener_por_id(tarea_id)
        self.assertIsNone(tarea_db_deleted, "La tarea no debería existir después de la eliminación.")
        
        # Verificar que las subtareas también fueron eliminadas (debido a cascade o eliminación explícita en el servicio)
        subtareas_despues_eliminacion = self.session.query(Subtarea).filter_by(tarea_id=tarea_id).all()
        self.assertEqual(len(subtareas_despues_eliminacion), 0, "Las subtareas de la tarea eliminada también deben ser eliminadas.")
        print(f"Tarea '{updated_titulo}' eliminada y verificada.")


# Para ejecutar las pruebas desde la línea de comandos
if __name__ == '__main__':
    # Asegurarse de que la base de datos se inicialice antes de ejecutar los tests
    # Esto es crucial para que Base.metadata.create_all(engine) tenga efecto
    # Si inicializar_base_de_datos() ya crea las tablas, esto puede ser redundante pero seguro.
    # En un entorno de pruebas con :memory:, es mejor que setUpClass maneje la creación.
    # crear_tablas() # Descomentar si no se usa setUpClass

    # Usamos argv para evitar que unittest.main() intente analizar argumentos de línea de comandos
    # que no son suyos, y exit=False para permitir que el script continúe después de las pruebas.
    unittest.main(argv=['first-arg-is-ignored'], exit=False)

