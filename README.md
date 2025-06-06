# 📋 Proyecto de Gestión de Tareas (TodoList)

Este proyecto es una aplicación CLI desarrollada en Python que permite gestionar tareas mediante operaciones CRUD (Crear, Leer, Actualizar, Eliminar) utilizando SQLAlchemy y SQLite. Se organiza con una arquitectura limpia basada en capas.

---

## 🧠 Modelo Conceptual

### Entidades:
- **Usuario**
  - `id`: Identificador único
  - `nombre_usuario`: Nombre del usuario (único, obligatorio)
  - `correo`: Correo electrónico (único, obligatorio)

- **Tarea**
  - `id`: Identificador único
  - `nombre`: Nombre de la tarea (obligatorio)
  - `descripcion`: Texto descriptivo
  - `fecha_creacion`, `fecha_limite`: Fechas
  - `completada`: Estado booleano
  - `usuario_id`: Clave foránea a Usuario

**Relación:** Un Usuario puede tener muchas Tareas (1:N).

---

## 🚀 Tecnologías Utilizadas

- Python 3.x
- SQLAlchemy (ORM)
- SQLite (`./data/database.db`)
- unittest (pruebas unitarias)

---

## 📁 Estructura del Proyecto

```
proyecto/
├── modelos/               # Entidades y esquemas de la base de datos
│   ├── usuario.py
│   └── tarea.py
├── repositorios/          # Operaciones CRUD
│   ├── usuario_repositorio.py
│   └── tarea_repositorio.py
├── servicios/             # Lógica de negocio
│   ├── usuario_servicio.py
│   └── tarea_servicio.py
├── pruebas/               # Pruebas unitarias
│   ├── test_usuario.py
│   └── test_tarea.py
├── database.py            # Configuración de SQLAlchemy
├── main.py                # Punto de entrada con menú interactivo
├── requirements.txt       # Dependencias necesarias
└── README.md              # Documentación del proyecto
```

---

## 🧩 Funcionalidades

- CRUD completo para las entidades `Usuario` y `Tarea`.
- Validaciones básicas: campos obligatorios, tipos de datos correctos.
- Menú interactivo en CLI (`main.py`):
  - Crear usuario
  - Crear tarea
  - Ver tareas de un usuario
  - Marcar tarea como completada
  - Eliminar tarea

---

## 🧪 Pruebas Unitarias

- Ubicadas en la carpeta `tests/`
- Ejecutan con:

```bash
python -m unittest discover tests
```

- Se usa base de datos **en memoria** (`sqlite:///:memory:`) para aislar los tests.
- Incluyen casos de éxito y fallo para validar la lógica de negocio.

---

## 🛠️ Instalación y Ejecución
0. Hacer Fork del Repositorio

    ##### a.Ve al repositorio original en GitHub.
    ##### b.Haz clic en el botón **"Fork"** en la parte superior derecha de la página.
    ##### c.GitHub creará automáticamente una copia del repositorio en tu propia cuenta.

1. Clona el repositorio:
```bash
git clone https://github.com/Tu_Repositorio/ProyectoFinal-ConstruccionDeSoftware.git
cd Proyecto_TodoList(Base de datos)
```

2. Crea entorno virtual e instala dependencias:
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Ejecuta el menú interactivo:
```bash
python main.py
```

---

## 👨‍👩‍👧‍👦 Integrantes del equipo

| Integrantes                   | 
|-------------------------------|
| ANCO PORRAS, Jhean Pier Julio |
| ISIDRO CASIO, Jose Luis       |
| LÓPEZ RODRIGUEZ, Axel Andre   |
|  MUNIVE RIOS, Antony          |
|SOTO ESCOBAR, Giancarlo Marcio|
|TUPAC GABINO, Julio Alberto Ricardo|



---

## 🔗 Repositorio GitHub

[Repositorio Publico del Proyecto](https://github.com/TONY-TUP4P1/ProyectoFinal-ConstruccionDeSoftware.git
)
