# Mi Agenda Universitaria
Este proyecto es una aplicación de escritorio desarrollada con Tkinter en Python, diseñada para ayudar a los estudiantes universitarios a gestionar sus tareas, subtareas y horarios de manera eficiente. La aplicación permite a los usuarios crear, editar, eliminar y organizar tareas, establecer prioridades, y mantener un seguimiento de su progreso. Utiliza SQLAlchemy para la persistencia de datos en una base de datos local SQLite.

# Características Principales
- Gestión de Usuarios: Registro e inicio de sesión para múltiples usuarios.
- Creación de Tareas: Define tareas con título, descripción, fecha límite, estado (pendiente/completada), prioridad y etiquetas.
- Subtareas: Desglosa tareas grandes en subtareas más pequeñas para un seguimiento detallado.
- Visualización de Tareas: Dashboard intuitivo para ver tareas pendientes y próximas.
- Edición y Eliminación: Funcionalidades completas para modificar y eliminar tareas y subtareas.
- Filtrado y Ordenamiento: Opciones para filtrar tareas por estado (vencidas, completadas) y ordenarlas por fecha.
- Persistencia de Datos: Almacenamiento seguro de toda la información en una base de datos SQLite.

# Requisitos del Sistema
Para ejecutar esta aplicación, necesitas tener Python instalado en tu sistema.

## Dependencias Principales
Puedes instalar las dependencias necesarias usando pip:

    pip install sqlalchemy>=1.4.0
    pip install Pillow>=9.0.0 # Necesaria para el manejo de imágenes (PIL/Pillow)


# Cómo Ejecutar el Proyecto
### Clona el repositorio:
    git clone <URL_DEL_REPOSITORIO>
    cd <NOMBRE_DEL_DIRECTORIO_DEL_PROYECTO>

### Instala las dependencias:
    pip install -r requirements.txt # (Si creas un archivo requirements.txt)
    # O instala manualmente:
    # pip install sqlalchemy Pillow

### Ejecuta la aplicación:

    python main.py

La aplicación se iniciará mostrando la pantalla de inicio de sesión/registro.

# Estructura del Proyecto
El proyecto sigue una arquitectura modular, con las siguientes carpetas principales:

- data/: Contiene la configuración de la base de datos y el archivo de la base de datos SQLite.

- modelos/: Define los modelos de la base de datos (Usuario, Tarea, Subtarea, Etiqueta, Categoría).

- repositorios/: Capa de acceso a datos que interactúa directamente con la base de datos.

- servicios/: Lógica de negocio que coordina entre la UI y los repositorios.

- validaciones/: Módulos con funciones para validar la entrada de datos.

- ui/: Contiene el archivo principal de la interfaz de usuario (ui.py) y sus componentes.

- img/: Almacena los recursos gráficos de la interfaz de usuario (logo, fondo, etc.).

- main.py: Punto de entrada principal de la aplicación.

# Contribuciones
Si deseas contribuir a este proyecto, puedes:

    1. Hacer un fork del repositorio.

    2. Crear una nueva rama (git checkout -b feature/nueva-caracteristica).

    3. Realizar tus cambios y asegurarte de que las pruebas pasen.

    4. Hacer commit de tus cambios (git commit -am 'feat: Añadir nueva característica').

    5. Push a la rama (git push origin feature/nueva-caracteristica).

    6. Abrir un Pull Request.

# Integrantes del Equipo
Este proyecto fue desarrollado por el siguiente equipo:

- Anco Porras Jhean Pier Julio

- Isidro Casio Jose Luis

- Lopez Rodriguez Axel Andre

- Munive Rios Antony

- Soto Escobar Giancarlo Murcio

- Tupac Gabino Julio Alberto Ricardo 

Declaramos que el trabajo desarrollado es de origen de equipo