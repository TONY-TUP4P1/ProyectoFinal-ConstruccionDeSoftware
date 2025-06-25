from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
import os

# Ruta relativa a la base de datos dentro de la carpeta 'data'
DATABASE_FILENAME = "Base De Datos.db"
DATABASE_PATH = os.path.join("data", DATABASE_FILENAME)
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# Configuración del motor
engine = create_engine(DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)

def listar_tablas():
    """Devuelve una lista de todas las tablas de la base de datos."""
    inspector = inspect(engine)
    return inspector.get_table_names()

def mostrar_datos_tabla(nombre_tabla):
    """Muestra todos los datos de una tabla específica, incluyendo los nombres de las columnas."""
    try:
        with engine.connect() as connection:
            print(f"\n--- Datos de la tabla: {nombre_tabla} ---")

            # Obtener los nombres de las columnas
            result = connection.execute(text(f"PRAGMA table_info({nombre_tabla})"))
            columnas_info = result.fetchall()
            nombres_columnas = [col[1] for col in columnas_info]

            if not nombres_columnas:
                print("No se encontraron columnas para esta tabla.")
                return

            print("| " + " | ".join(nombres_columnas) + " |")
            print("|" + "---|".join(['-' * len(col) for col in nombres_columnas]) + "|")

            # Obtener y mostrar los datos
            result = connection.execute(text(f"SELECT * FROM {nombre_tabla}"))
            filas = result.fetchall()

            if not filas:
                print("No hay datos en esta tabla.")
            else:
                for fila in filas:
                    print("| " + " | ".join(map(str, fila)) + " |")

    except Exception as e:
        print(f"Error al leer la tabla {nombre_tabla}: {e}")

if __name__ == "__main__":
    if not os.path.exists(DATABASE_PATH):
        print(f"La base de datos '{DATABASE_FILENAME}' no existe en la carpeta 'data'.")
        print(f"Asegúrate de que el archivo '{DATABASE_FILENAME}' esté ubicado en la ruta: {DATABASE_PATH}")
    else:
        todas_las_tablas = listar_tablas()
        if todas_las_tablas:
            print(f"Tablas encontradas en la base de datos '{DATABASE_FILENAME}':")
            for tabla in todas_las_tablas:
                print(f"- {tabla}")
                mostrar_datos_tabla(tabla)
        else:
            print("No se encontraron tablas en la base de datos.")
