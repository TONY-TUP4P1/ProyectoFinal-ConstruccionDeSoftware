"""
main.py

Archivo principal del proyecto. Inicia la creación de la base de datos y lanza el menú interactivo
para la gestión de tareas mediante consola. Utiliza servicios y repositorios para acceder y operar
sobre los datos de usuarios, tareas, subtareas, etiquetas y categorías.

Ejecución:
    python main.py
"""

from datetime import datetime, timedelta
import os
from database import Base, engine, get_session
from modelos.tarea import NivelPrioridad
from repositorios import (CategoriaRepositorio,
                          EtiquetaRepositorio,
                          SubtareaRepositorio,
                          TareaRepositorio,
                          UsuarioRepositorio)
from servicios import (CategoriaServicio,
                       EtiquetaServicio,
                       SubtareaServicio,
                       TareaServicio,
                       UsuarioServicio)


def crear_base_de_datos():
    """Crea todas las tablas en la base de datos si no existen."""
    from modelos import usuario, tarea, subtarea, etiqueta, categoria, tareas_etiquetas
    Base.metadata.create_all(bind=engine)



def inicializar_servicios():
    """Inicializa repositorios y servicios, y retorna todos los objetos necesarios."""
    sesion = get_session()
    usuario_repo = UsuarioRepositorio(sesion)
    tarea_repo = TareaRepositorio(sesion)
    subtarea_repo = SubtareaRepositorio(sesion)
    categoria_repo = CategoriaRepositorio(sesion)
    etiqueta_repo = EtiquetaRepositorio(sesion)

    usuario_service = UsuarioServicio(usuario_repo)
    tarea_service = TareaServicio(tarea_repo, usuario_repo)
    subtarea_service = SubtareaServicio(subtarea_repo, tarea_repo)
    categoria_service = CategoriaServicio(categoria_repo)
    etiqueta_service = EtiquetaServicio(etiqueta_repo)

    return (sesion, usuario_service,
            tarea_service, subtarea_service,
            categoria_service, etiqueta_service)

def crear_usuario_demo(usuario_service):
    """Crea un usuario demo para pruebas."""
    return usuario_service.registrar_usuario(
        nombre="Antony",
        apellido="Munive",
        correo="72310206@continental.edu.pe",
        contrasena="72310206"
    )

def mostrar_menu():
    """Muestra el menú principal."""
    print("\n--- MENÚ PRINCIPAL ---")
    print("1. Crear tarea")
    print("2. Ver tareas completadas")
    print("3. Ver tareas pendientes")
    print("4. Ver tareas que vencen hoy")
    print("5. Ver tareas por rango de fecha")
    print("6. Crear subtarea")
    print("7. Crear categoría")
    print("8. Crear etiqueta")
    print("9. Asignar etiqueta a tarea")
    print("10. Salir")

def opcion_crear_tarea(tarea_service, usuario, tareas_creadas):
    """
    Permite al usuario crear una nueva tarea con:
     título, descripción, prioridad y fecha límite.
     """
    titulo = input("Título: ")
    descripcion = input("Descripción: ")
    dias = int(input("¿En cuántos días vence? "))
    prioridad_input = input("Prioridad (ALTA, MEDIA, BAJA): ").upper()
    try:
        prioridad_enum = NivelPrioridad[prioridad_input]
    except KeyError:
        print("❌ Prioridad inválida. Se usará MEDIA por defecto.")
        prioridad_enum = NivelPrioridad.MEDIA

    tarea = tarea_service.crear_tarea(
        usuario_id=usuario.id,
        titulo=titulo,
        descripcion=descripcion,
        fecha_limite=datetime.now().date() + timedelta(days=dias),
        prioridad=prioridad_enum
    )
    tareas_creadas.append(tarea)
    print("✅ Tarea creada.")

def opcion_listar_tareas(tarea_service, usuario, estado):
    """Muestra las tareas completadas o pendientes, según el valor booleano de 'estado'."""
    tareas = tarea_service.obtener_tareas_por_estado(usuario.id, estado)
    estado_texto = "completadas" if estado else "pendientes"
    print(f"\n📋 Tareas {estado_texto}:")
    for t in tareas:
        print(f"- {t.titulo} ({t.prioridad.value})")

def opcion_tareas_hoy(tarea_service, usuario):
    """Muestra las tareas del usuario que vencen en la fecha actual."""
    tareas = tarea_service.obtener_tareas_que_vencen_hoy(usuario.id)
    print("\n📅 Tareas que vencen hoy:")
    for t in tareas:
        print(f"- {t.titulo}")

def opcion_tareas_rango(tarea_service, usuario):
    """Muestra tareas cuya fecha límite está dentro de un rango de días definido por el usuario."""
    dias_inicio = int(input("¿Desde cuántos días inicia el rango?: "))
    dias_fin = int(input("¿Hasta cuántos días desde hoy?: "))
    inicio = datetime.now().date() + timedelta(days=dias_inicio)
    fin = datetime.now().date() + timedelta(days=dias_fin)
    tareas = tarea_service.obtener_tareas_por_rango(usuario.id, inicio, fin)
    print(f"\n🗓️ Tareas entre {inicio} y {fin}:")
    for t in tareas:
        print(f"- {t.titulo} (vence: {t.fecha_limite})")

def opcion_crear_subtarea(subtarea_service, tareas_creadas):
    """Crea una subtarea asociada a una tarea seleccionada por el usuario."""
    if not tareas_creadas:
        print("⚠️ Primero crea al menos una tarea.")
        return
    for i, t in enumerate(tareas_creadas):
        print(f"{i+1}. {t.titulo}")
    index = int(input("Seleccione tarea (N°): ")) - 1
    titulo = input("Título de la subtarea: ")
    subtarea_service.crear_subtarea(tarea_id=tareas_creadas[index].id, titulo=titulo)
    print("✅ Subtarea creada.")

def opcion_crear_categoria(categoria_service):
    """Permite al usuario crear una nueva categoría."""
    nombre = input("Nombre de la categoría: ")
    categoria = categoria_service.crear_categoria(nombre)
    print(f"✅ Categoría '{categoria.nombre}' creada.")

def opcion_crear_etiqueta(etiqueta_service):
    """Permite al usuario crear una nueva etiqueta."""
    nombre = input("Nombre de la etiqueta: ")
    etiqueta = etiqueta_service.crear_etiqueta(nombre)
    print(f"✅ Etiqueta '{etiqueta.nombre}' creada.")

def opcion_asignar_etiqueta(etiqueta_service, tareas_creadas, sesion):
    """Asigna una etiqueta existente a una tarea seleccionada por el usuario."""
    if not tareas_creadas:
        print("⚠️ Primero crea una tarea.")
        return
    for i, t in enumerate(tareas_creadas):
        print(f"{i+1}. {t.titulo}")
    tarea_idx = int(input("Seleccione tarea (N°): ")) - 1
    etiqueta_nombre = input("Nombre de etiqueta a asignar: ")
    etiqueta = etiqueta_service.obtener_por_nombre(etiqueta_nombre)
    if etiqueta:
        tareas_creadas[tarea_idx].etiquetas.append(etiqueta)
        sesion.commit()
        print("✅ Etiqueta asignada.")
    else:
        print("❌ Etiqueta no encontrada.")

def ejecutar_prueba():
    """Controla el menú interactivo del sistema."""
    (sesion, usuario_service, tarea_service,
     subtarea_service, categoria_service,
     etiqueta_service) = inicializar_servicios()
    usuario = crear_usuario_demo(usuario_service)
    tareas_creadas = []

    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            opcion_crear_tarea(tarea_service, usuario, tareas_creadas)
            return ejecutar_prueba()
        elif opcion == "2":
            opcion_listar_tareas(tarea_service, usuario, True)
        elif opcion == "3":
            opcion_listar_tareas(tarea_service, usuario, False)
        elif opcion == "4":
            opcion_tareas_hoy(tarea_service, usuario)
        elif opcion == "5":
            opcion_tareas_rango(tarea_service, usuario)
        elif opcion == "6":
            opcion_crear_subtarea(subtarea_service, tareas_creadas)
        elif opcion == "7":
            opcion_crear_categoria(categoria_service)
        elif opcion == "8":
            opcion_crear_etiqueta(etiqueta_service)
        elif opcion == "9":
            opcion_asignar_etiqueta(etiqueta_service, tareas_creadas, sesion)
        elif opcion == "10":
            print("👋 Hasta luego.")
            break
        else:
            print("❌ Opción no válida.")

if __name__ == "__main__":
    # Ruta al archivo de base de datos
    DB_PATH = "./data/database.db"

    # Elimina la base de datos si ya existe
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    crear_base_de_datos()
    ejecutar_prueba()
