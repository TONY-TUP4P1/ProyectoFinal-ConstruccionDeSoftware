from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from modelos.usuario import Usuario
from modelos.tarea import Tarea
from servicios.usuario_servicio import registrar_usuario, obtener_perfil_usuario
from servicios.tarea_servicio import crear_nueva_tarea, ver_tareas_usuario, marcar_tarea_como_completada, \
    eliminar_una_tarea

# Configuración de la base de datos
DATABASE_URL = "sqlite:///./data/database.db"  # Usando base de datos

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Crear las tablas
from database import Base

Base.metadata.create_all(bind=engine)


# Función para crear un usuario
def crear_usuario():
    nombre_usuario = input("Ingresa el nombre de usuario: ")
    correo = input("Ingresa el correo: ")
    session = SessionLocal()
    usuario = registrar_usuario(session, nombre_usuario, correo)
    print(f"Usuario creado: {usuario.nombre_usuario}, {usuario.correo}")
    session.close()


# Función para crear una tarea
def crear_tarea():
    usuario_id = input("Ingresa el ID del usuario para la tarea: ")
    nombre_tarea = input("Ingresa el nombre de la tarea: ")
    descripcion_tarea = input("Ingresa la descripción de la tarea: ")
    session = SessionLocal()
    tarea = crear_nueva_tarea(session, nombre_tarea, descripcion_tarea, usuario_id)
    print(f"Tarea creada: {tarea.nombre}, {tarea.descripcion}")
    session.close()


# Función para ver las tareas de un usuario
def ver_tareas():
    usuario_id = input("Ingresa el ID del usuario para ver sus tareas: ")
    session = SessionLocal()
    tareas = ver_tareas_usuario(session, usuario_id)
    print("Tareas:")
    for tarea in tareas:
        print(f"{tarea.id}. {tarea.nombre} - {tarea.descripcion} - Completada: {tarea.completada}")
    session.close()


# Función para marcar tarea como completada
def completar_tarea():
    tarea_id = input("Ingresa el ID de la tarea para marcar como completada: ")
    session = SessionLocal()
    tarea = marcar_tarea_como_completada(session, tarea_id)
    print(f"Tarea {tarea.id} marcada como completada.")
    session.close()


# Función para eliminar tarea
def eliminar_tarea():
    tarea_id = input("Ingresa el ID de la tarea para eliminar: ")
    session = SessionLocal()
    tarea = eliminar_una_tarea(session, tarea_id)
    print(f"Tarea {tarea.id} eliminada.")
    session.close()


# Menú de opciones
def menu():
    while True:
        print("\nMenú de Opciones")
        print("1. Crear usuario")
        print("2. Crear tarea")
        print("3. Ver tareas de un usuario")
        print("4. Marcar tarea como completada")
        print("5. Eliminar tarea")
        print("6. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            crear_usuario()
        elif opcion == "2":
            crear_tarea()
        elif opcion == "3":
            ver_tareas()
        elif opcion == "4":
            completar_tarea()
        elif opcion == "5":
            eliminar_tarea()
        elif opcion == "6":
            print("Saliendo del programa...")
            break
        else:
            print("Opción no válida. Por favor, selecciona una opción válida.")


# Ejecutar el menú
if __name__ == "__main__":
    menu()
