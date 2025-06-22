from database import Base, engine
from modelos import tarea, usuario, subtarea, etiqueta, categoria, tareas_etiquetas

print("🛠️ Creando base de datos...")
Base.metadata.create_all(bind=engine)
print("✅ Tablas creadas correctamente.")
