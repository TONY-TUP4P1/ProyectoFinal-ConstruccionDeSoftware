# main.py
from data.database import crear_tablas
from ui import iniciar_aplicacion

if __name__ == "__main__":
    crear_tablas()            # ✅ Asegura la creación de tablas antes de iniciar la app
    iniciar_aplicacion()      # ⬅️ Ejecuta la interfaz
