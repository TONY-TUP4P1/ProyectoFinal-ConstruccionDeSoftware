from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from modelos.base import Base
from modelos.usuario import Usuario
from modelos.tarea import Tarea, PrioridadEnum
from servicios.usuario_servicio import UsuarioService
from servicios.tarea_servicio import TareaService
from servicios.subtarea_servicio import SubTareaService
from servicios.categoria_servicio import CategoriaService
from servicios.etiqueta_servicio import EtiquetaService
from datetime import datetime
import os

DATABASE_URL = "sqlite:///data/database.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()

def menu():
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Crear usuario")
    print("2. Crear tarea")
    print("3. Ver usuarios")
    print("4. Ver tareas")
    print("5. Salir")
    print("6. Asignar subtarea")
    print("7. Asignar categoría")
    print("8. Asignar etiqueta")

    return input("Selecciona una opción: ")

def crear_usuario(usuario_service):
    print("\n--- Crear Usuario ---")
    id = input("ID: ")
    nombre = input("Nombre: ")
    apellido = input("Apellido: ")
    contrasena = input("Contraseña: ")
    correo = input("Correo: ")
    telefono = input("Teléfono: ")
    fecha_nacimiento = input("Fecha de nacimiento (YYYY-MM-DD): ")

    usuario = Usuario(
        id=id,
        nombre=nombre,
        apellido=apellido,
        contrasena=contrasena,
        correo=correo,
        telefono=telefono,
        fecha_nacimiento=datetime.strptime(fecha_nacimiento, "%Y-%m-%d")
    )
    usuario_service.registrar(usuario)
    print("✅ Usuario creado.")

def crear_tarea(tarea_service):
    print("\n--- Crear Tarea ---")
    id = input("ID: ")
    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    usuario_id = input("ID del usuario: ")
    prioridad = input("Prioridad (baja, media, alta): ").lower()

    tarea = Tarea(
        id=id,
        titulo=titulo,
        descripcion=descripcion,
        fecha_creacion=datetime.now(),
        fecha_limite=datetime.now(),
        estado=False,
        usuario_id=usuario_id,
        prioridad=PrioridadEnum(prioridad)
    )
    tarea_service.crear_tarea(tarea)
    print("✅ Tarea creada.")

def ver_usuarios(usuario_service):
    print("\n--- Lista de Usuarios ---")
    usuarios = usuario_service.repo.session.query(Usuario).all()
    for u in usuarios:
        print(f"{u.id} - {u.nombre} {u.apellido} ({u.correo})")

def ver_tareas(tarea_service):
    print("\n--- Lista de Tareas ---")
    tareas = tarea_service.repo.session.query(Tarea).all()
    for t in tareas:
        print(f"{t.id} - {t.titulo} | Prioridad: {t.prioridad.value} | Estado: {'✅' if t.estado else '❌'}")

def asignar_subtarea(subtarea_service):
    print("\n--- Asignar Subtarea ---")
    id = input("ID de la subtarea: ")
    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    tarea_id = input("ID de la tarea: ")

    subtarea = subtarea_service(
        id=id,
        titulo=titulo,
        descripcion=descripcion,
        completada=False,
        tarea_id=tarea_id
    )
    subtarea_service.crear_subtarea(subtarea)
    print("✅ Subtarea asignada.")

def asignar_categoria(categoria_service, tarea_service):
    print("\n--- Asignar Categoría ---")
    categoria_id = input("ID de la categoría: ")
    nombre = input("Nombre de la categoría: ")
    tarea_id = input("ID de la tarea: ")

    categoria = categoria_service(id=categoria_id, nombre=nombre)
    categoria_service.asignar_categoria(categoria)

    tarea = tarea_service.obtener_tarea(tarea_id)
    if tarea:
        tarea.categoria_id = categoria_id
        tarea_service.repo.update(tarea)
        print("✅ Categoría asignada a la tarea.")
    else:
        print("❌ Tarea no encontrada.")

def asignar_etiqueta(etiqueta_service):
    print("\n--- Asignar Etiqueta ---")
    id = input("ID de la etiqueta: ")
    nombre = input("Nombre: ")
    tarea_id = input("ID de la tarea: ")

    etiqueta = etiqueta_service(id=id, nombre=nombre, tarea_id=tarea_id)
    etiqueta_service.asignar_etiqueta(etiqueta)
    print("✅ Etiqueta asignada.")


if __name__ == "__main__":
    session = init_db()
    usuario_service = UsuarioService(session)
    tarea_service = TareaService(session)
    subtarea_service = SubTareaService(session)
    categoria_service = CategoriaService(session)
    etiqueta_service = EtiquetaService(session)

    while True:
        opcion = menu()
        if opcion == "1":
            crear_usuario(usuario_service)
        elif opcion == "2":
            crear_tarea(tarea_service)
        elif opcion == "3":
            ver_usuarios(usuario_service)
        elif opcion == "4":
            ver_tareas(tarea_service)
        elif opcion == "5":
            print("👋 ¡Hasta luego!")
        elif opcion == "6":
            asignar_subtarea(subtarea_service)
        elif opcion == "7":
            asignar_categoria(categoria_service, tarea_service)
        elif opcion == "8":
            asignar_etiqueta(etiqueta_service)
            break
        else:
            print("❌ Opción no válida.")
