# data/database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import sqlite3 # Importar para manejo directo de errores de SQLite

# Crear la carpeta 'data' si no existe
os.makedirs("data", exist_ok=True)

# Ruta de la base de datos dentro de la carpeta 'data'
DATABASE_URL = "sqlite:///data/Base De Datos.db"

# Crear el motor de conexión
# connect_args={"check_same_thread": False} es necesario para SQLite en entornos de múltiples hilos
# como Tkinter, que ejecuta callbacks en el hilo principal.
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Crear el generador de sesiones
# expire_on_commit=False es útil para que los objetos no se 'expiren' automáticamente
# después de un commit, permitiendo acceder a sus atributos fuera de la sesión que los cargó.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Clase base para los modelos
Base = declarative_base()

# Función para crear las tablas
def crear_tablas():
    # Importar todos los modelos aquí para asegurar que Base.metadata los conozca
    # antes de crear las tablas.
    from modelos.usuario import Usuario
    from modelos.tarea import Tarea
    from modelos.subtarea import Subtarea
    from modelos.categoria import Categoria
    from modelos.etiqueta import Etiqueta

    # Llamar a create_all para crear todas las tablas definidas en Base.metadata
    # Esto buscará todas las clases que heredan de Base y creará sus tablas si no existen.
    Base.metadata.create_all(bind=engine)
    print("Tablas de la base de datos creadas o ya existentes.")

# Función para inicializar la base de datos con validación
def inicializar_base_de_datos():
    db_path = DATABASE_URL.replace("sqlite:///", "") # Obtener la ruta del archivo de la DB

    if os.path.exists(db_path):
        print(f"Base de datos encontrada en: {db_path}")
        try:
            # Intentar conectar y ejecutar una operación simple para verificar la integridad
            test_conn = sqlite3.connect(db_path)
            test_cursor = test_conn.cursor()
            # Intenta obtener una lista de tablas. Si la DB está corrupta, esto fallará.
            test_cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            test_conn.close()
            print("Base de datos existente es accesible y parece estar bien.")
        except sqlite3.Error as e:
            print(f"Error al acceder a la base de datos (posiblemente corrupta o esquema incompatible): {e}")
            print("Base de datos eliminada. Se recreará.")
            os.remove(db_path) # Eliminar el archivo corrupto
            # Considera añadir un mensaje de error visual si esto ocurre en una aplicación GUI
            # por ejemplo, con messagebox.showwarning en tkinter.
        finally:
            if test_conn:
                test_conn.close() # Asegurarse de cerrar la conexión de prueba

    # Llamar a crear_tablas (creará si no existe o si fue eliminada)
    crear_tablas()
    print("Verificación y creación de tablas completada.")

