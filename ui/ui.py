import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import datetime, date # Import date for clearer usage
import uuid
import os
# import re # No se usa directamente en el código de la UI, se podría remover si no es usado por validaciones externas
# import sqlite3 # Mantener por si acaso, aunque la lógica principal se movió. Si no se usa en otra parte de UI, se puede quitar.

# Asegúrate de que las rutas a tus módulos de base de datos y servicios sean correctas
# Suponiendo que 'data' y 'modelos' están en el mismo directorio que este script, o en un PYTHONPATH accesible.
try:
    from data.database import SessionLocal, inicializar_base_de_datos, DATABASE_URL # Importar inicializar_base_de_datos
    from modelos.usuario import Usuario
    from modelos.tarea import Tarea, PrioridadEnum # Importar PrioridadEnum
    # Asegúrate de que tu modelo Tarea acepte 'tarea_id' como PK y tenga una relación 'usuario'
    # También, que el modelo Subtarea maneje 'completada' como booleano
    from servicios.usuario_servicio import UsuarioService
    from servicios.tarea_servicio import TareaService
    from validaciones.correo import validar_correo
    from validaciones.contraseña import validar_contrasena
    from validaciones.celular import validar_numero_celular
    from validaciones.fecha import validar_fecha
    from validaciones.texto import validar_texto_no_vacio
except ImportError as e:
    messagebox.showerror("Error de Importación", f"No se pudieron importar módulos de la base de datos: {e}\n"
                                               "Asegúrate de que 'data', 'modelos' y 'servicios' "
                                               "estén en el PYTHONPATH o en el mismo directorio.")
    exit()

# --- Inicializar la Base de Datos ---
# Esta función ahora maneja la verificación y recreación si es necesario.
inicializar_base_de_datos()

# --- Sesión DB y Servicios ---
session = SessionLocal()
usuario_service = UsuarioService(session)
tarea_service = TareaService(session)


usuario_actual = None # Almacena el objeto Usuario del usuario actualmente logueado

# --- Ventana principal ---
root = tk.Tk()
root.title("Mi Agenda Universitaria")
root.geometry("800x620")
root.resizable(False, False)

# --- Fondo de la aplicación ---
try:
    # Intenta cargar el fondo con LANCZOS para mejor calidad
    fondo_img = Image.open("img/fondo.jpg").resize((800, 650), Image.LANCZOS)
    fondo = ImageTk.PhotoImage(fondo_img)
    canvas = tk.Canvas(root, width=800, height=650)
    canvas.pack(fill="both", expand=True)
    canvas.create_image(0, 0, image=fondo, anchor="nw")
except Exception:
    # Si falla, usa un color sólido de fondo
    canvas = tk.Canvas(root, width=800, height=650, bg="#2c3e50") # Un gris oscuro atractivo
    canvas.pack(fill="both", expand=True)

# --- Header ---
header_frame = tk.Frame(root, bg="white", height=80, width=800)
header_frame.place(x=0, y=0)

# Cargar y mostrar logo
logo_path = "img/logo.png" # Asegúrate de que la ruta sea correcta
if os.path.exists(logo_path):
    try:
        logo_img = Image.open(logo_path).resize((60, 60), Image.LANCZOS)
        logo = ImageTk.PhotoImage(logo_img)
        tk.Label(header_frame, image=logo, bg="white").place(x=10, y=10)
    except Exception as e:
        print(f"Error al cargar el logo: {e}")
        # En caso de error, no mostrar imagen pero continuar

tk.Label(header_frame, text="MI AGENDA UNIVERSITARIA", font=("Arial", 16, "bold"), bg="white").place(relx=0.5, rely=0.5, anchor="center")

header_label_right = tk.Label(header_frame, text="INICIAR SESIÓN", font=("Arial", 11, "bold"), bg="white")
header_label_right.place(x=650, y=30)

cerrar_sesion_btn = tk.Button(header_frame, text="Cerrar sesión ⏎", bg="#d32f2f", fg="white", font=("Arial", 10, "bold"), command=lambda: cerrar_sesion())


# --- Variables globales para la UI y datos de tarea ---
tareas_creadas = [] # Esta lista ahora se poblará desde la base de datos
tarea_index_actual = None # Índice de la tarea que se está editando
subtarea_widgets_editar = [] # Para manejar subtareas en edición


# --- Funciones de navegación de vistas ---
def cambiar_vista(vista_frame):
    """Oculta todos los frames de vista y muestra el especificado."""
    # Lista de todos los frames de vista para gestionarlos
    all_view_frames = [login_frame, registro_frame, dashboard_frame, crear_tarea_frame, editar_tarea_frame, ver_tareas_frame]
    for frame in all_view_frames:
        frame.place_forget() # Oculta todos los frames

    vista_frame.place(x=0, y=80, width=800, height=540) # Posiciona el frame deseado

    # Ajustes específicos para cada vista
    if vista_frame == login_frame:
        header_label_right.config(text="INICIAR SESIÓN")
        header_label_right.place(x=650, y=30)
        cerrar_sesion_btn.place_forget()
        login_frame.place(x=260, y=180, width=300, height=230) # Ajuste de tamaño para login
    elif vista_frame == registro_frame:
        header_label_right.config(text="REGISTRAR USUARIO")
        header_label_right.place(x=615, y=30)
        cerrar_sesion_btn.place_forget()
        registro_frame.place(x=200, y=100, width=450, height=490) # Ajuste de tamaño para registro
    elif vista_frame == dashboard_frame:
        header_label_right.place_forget() # No label derecho en dashboard
        cerrar_sesion_btn.place(x=670, y=25)
        # El dashboard ahora es el frame principal después del login
        dashboard_frame.place(x=0, y=80, width=800, height=540) # Ocupa toda el área principal
        actualizar_dashboard()
    elif vista_frame == crear_tarea_frame:
        header_label_right.config(text="CREAR TAREA")
        header_label_right.place(x=650, y=30)
        cerrar_sesion_btn.place_forget()
        # Resetear campos de crear tarea
        entry_crear_titulo.delete(0, tk.END)
        entry_crear_fecha.delete(0, tk.END)
        var_crear_estado.set("Pendiente") # Resetear OptionMenu
        var_crear_prioridad.set("MEDIA")  # Resetear OptionMenu
        entry_crear_etiqueta.delete(0, tk.END)
        text_crear_descripcion.delete("1.0", tk.END)
        # Limpiar subtareas
        for entry in subtareas_entries:
            entry.destroy()
        subtareas_entries.clear()

        crear_tarea_frame.place(x=175, y=120, width=450, height=460) # Ajuste de tamaño para crear tarea
        canvas_crear.update_idletasks()
        canvas_crear.configure(scrollregion=canvas_crear.bbox("all"))
        canvas_crear.yview_moveto(0)
    elif vista_frame == editar_tarea_frame:
        header_label_right.config(text="EDITAR TAREA")
        header_label_right.place(x=650, y=30)
        cerrar_sesion_btn.place_forget()
        editar_tarea_frame.place(x=175, y=120, width=450, height=500) # Ajuste de tamaño para editar tarea
        canvas_editar.update_idletasks()
        canvas_editar.configure(scrollregion=canvas_editar.bbox("all"))
        canvas_editar.yview_moveto(0)
    elif vista_frame == ver_tareas_frame:
        header_label_right.place_forget()
        cerrar_sesion_btn.place(x=670, y=25)
        ver_tareas_frame.place(x=0, y=80, width=800, height=540)
        actualizar_tareas_ver()


# --- Funciones de Placeholder para Entry widgets ---
def on_entry_focus_in(e, entry_widget, placeholder_text, is_password=False):
    if entry_widget.get() == placeholder_text:
        entry_widget.delete(0, tk.END)
        entry_widget.config(fg="black", show="*" if is_password else "")

def on_entry_focus_out(e, entry_widget, placeholder_text, is_password=False):
    if entry_widget.get() == "":
        entry_widget.insert(0, placeholder_text)
        entry_widget.config(fg="gray", show="*" if is_password else "")


# --- LOGIN ---
login_frame = tk.Frame(root, bg="white")

tk.Label(login_frame, text="Correo Electrónico:", font=("Arial", 10), bg="white", anchor="w").pack(fill="x", padx=53, pady=(10, 2))
entry_login_correo = tk.Entry(login_frame, width=30, fg="gray", justify="left")
entry_login_correo.insert(0, "Ingrese su Correo Electrónico")
entry_login_correo.pack(padx=10, pady=2)
entry_login_correo.bind("<FocusIn>", lambda e: on_entry_focus_in(e, entry_login_correo, "Ingrese su Correo Electrónico"))
entry_login_correo.bind("<FocusOut>", lambda e: on_entry_focus_out(e, entry_login_correo, "Ingrese su Correo Electrónico"))

tk.Label(login_frame, text="Contraseña:", font=("Arial", 10), bg="white", anchor="w").pack(fill="x", padx=53, pady=(10, 2))
entry_login_pass = tk.Entry(login_frame, width=30, fg="gray", justify="left")
entry_login_pass.insert(0, "Ingrese su contraseña")
entry_login_pass.pack(padx=10, pady=2)
entry_login_pass.bind("<FocusIn>", lambda e: on_entry_focus_in(e, entry_login_pass, "Ingrese su contraseña", True))
entry_login_pass.bind("<FocusOut>", lambda e: on_entry_focus_out(e, entry_login_pass, "Ingrese su contraseña", True))

def login():
    global usuario_actual
    correo = entry_login_correo.get().strip()
    contrasena = entry_login_pass.get().strip()

    if not all([correo, contrasena]) or correo == "Ingrese su Correo Electrónico" or contrasena == "Ingrese su contraseña":
        messagebox.showwarning("Faltan datos", "Completa todos los campos.")
        return

    _, err_correo = validar_correo(correo)
    if err_correo:
        messagebox.showerror("Error de Validación", err_correo)
        return

    _, err_pass = validar_contrasena(contrasena) # Puedes omitir esto si la validación de contraseña es solo en registro
    if err_pass:
        messagebox.showerror("Error de Validación", err_pass)
        return

    usuario = usuario_service.buscar_por_correo(correo)
    if usuario and usuario.contrasena == contrasena: # NOTA: En un sistema real, usa hashing para contraseñas
        usuario_actual = usuario
        messagebox.showinfo("Bienvenido", f"¡Hola {usuario.nombre}!")
        cambiar_vista(dashboard_frame)
    else:
        messagebox.showerror("Error de Sesión", "Correo o contraseña incorrectos.")

tk.Button(login_frame, text="INICIAR SESIÓN", bg="#4CAF50", fg="white", width=25, command=login, cursor="hand2").pack(pady=15)
tk.Button(login_frame, text="¿No tienes cuenta? Regístrate", bg="white", fg="gray", bd=0, font=("Arial", 9), command=lambda: cambiar_vista(registro_frame), cursor="hand2").pack()


# --- REGISTRO ---
registro_frame = tk.Frame(root, bg="white")
campos_registro = [
    ("Nombre Completo:", "Ingrese su nombre completo (Nombres y Apellidos)", False),
    ("Correo Electrónico:", "Ingrese su Correo Electrónico", False),
    ("Contraseña:", "Ingrese una contraseña", True),
    ("Confirmar Contraseña:", "Reescriba su contraseña", True),
    ("Teléfono:", "Ingrese su número de celular", False),
    ("Fecha de Nacimiento:", "dd/mm/aaaa", False)
]
reg_entries = {} # Diccionario para almacenar los Entry widgets del registro

# Mapping of display labels to internal keys, handling special characters for internal keys
# This dictionary will map the 'display_label' to a 'cleaned_key'
reg_field_keys = {
    "Nombre Completo:": "nombre_completo",
    "Correo Electrónico:": "correo_electronico",
    "Contraseña:": "contrasena", # Using 'contrasena' without 'ñ' for key consistency
    "Confirmar Contraseña:": "confirmar_contrasena", # Using 'contrasena' without 'ñ'
    "Teléfono:": "telefono", # Using 'telefono' without 'ó'
    "Fecha de Nacimiento:": "fecha_de_nacimiento"
}


for i, (etiqueta_text, placeholder, is_password) in enumerate(campos_registro):
    tk.Label(registro_frame, text=etiqueta_text, font=("Arial", 10), bg="white", anchor="w").pack(
        fill="x", padx=68, pady=(8 if i else 10, 0))

    entry = tk.Entry(registro_frame, width=50, fg="gray", show="*" if is_password else "")
    entry.insert(0, placeholder)
    entry.bind("<FocusIn>", lambda e, ent=entry, ph=placeholder, pw=is_password: on_entry_focus_in(e, ent, ph, pw))
    entry.bind("<FocusOut>", lambda e, ent=entry, ph=placeholder, pw=is_password: on_entry_focus_out(e, ent, ph, pw))
    entry.pack(padx=45, pady=(0, 5))
    
    # Store entry using the clean key from reg_field_keys
    if etiqueta_text in reg_field_keys:
        reg_entries[reg_field_keys[etiqueta_text]] = entry
    else:
        # Fallback if a new field is added without a mapping, though less ideal
        cleaned_key = etiqueta_text.lower().replace(":", "").replace(" ", "_")
        reg_entries[cleaned_key] = entry


def registrar():
    # DEBUG: Print keys in reg_entries to see what's actually there
    print(f"Keys in reg_entries before access: {reg_entries.keys()}")

    # Retrieve values using the defined keys
    # Se agrega una verificación antes de acceder a la clave para evitar KeyError
    try:
        nombre_completo = reg_entries["nombre_completo"].get().strip()
        correo = reg_entries["correo_electronico"].get().strip()
        pass1 = reg_entries["contrasena"].get() # Accessing with 'contrasena'
        pass2 = reg_entries["confirmar_contrasena"].get() # Accessing with 'contrasena'
        telefono = reg_entries["telefono"].get().strip() # Accessing with 'telefono'
        fecha_str = reg_entries["fecha_de_nacimiento"].get().strip()
    except KeyError as e:
        messagebox.showerror("Error de Formulario", f"Falta un campo requerido en el formulario de registro: {e}. Por favor, reinicia la aplicación o contacta al soporte.")
        return


    # Validate against placeholders using the mapped keys
    # Iterate through campos_registro to get original placeholder text,
    # then map to the correct reg_entries key
    for etiqueta_text, placeholder, _ in campos_registro:
        # Get the cleaned key using the mapping, or fallback to direct cleaning
        cleaned_key = reg_field_keys.get(etiqueta_text, etiqueta_text.lower().replace(":", "").replace(" ", "_"))
        
        # Check if the key exists in reg_entries before accessing
        if cleaned_key not in reg_entries:
            # Esto ya se maneja con el try-except superior, pero se mantiene como una doble verificación.
            messagebox.showerror("Error Interno", f"Falta el campo '{etiqueta_text}' en el formulario. Por favor, reinicia la aplicación.")
            return

        if reg_entries[cleaned_key].get().strip() == placeholder:
            messagebox.showwarning("Error", "Por favor, completa todos los campos (quita los textos de ejemplo).")
            return

    if not all([nombre_completo, correo, pass1, pass2, telefono, fecha_str]):
        messagebox.showwarning("Error", "Completa todos los campos.")
        return

    if pass1 != pass2:
        messagebox.showwarning("Error", "Las contraseñas no coinciden.")
        return

    # Validaciones individuales
    validations = [
        (validar_correo, correo, "Error de Correo"),
        (validar_contrasena, pass1, "Error de Contraseña"),
        (validar_numero_celular, telefono, "Error de Teléfono"),
        (validar_fecha, fecha_str, "Error de Fecha")
    ]

    for validator, value, error_title in validations:
        _, err = validator(value)
        if err:
            messagebox.showerror(error_title, err)
            return

    try:
        fecha_nacimiento_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Error de Fecha", "Formato de fecha inválido. Usa dd/mm/aaaa.")
        return

    nombre, apellido = (nombre_completo.split(" ", 1) + [""])[:2] # Divide nombre y apellido

    nuevo_usuario = Usuario(
        id=str(uuid.uuid4()),
        nombre=nombre,
        apellido=apellido,
        correo=correo,
        contrasena=pass1, # En un sistema real, usa hashing de contraseñas
        telefono=telefono,
        fecha_nacimiento=fecha_nacimiento_obj
    )

    if usuario_service.registrar_usuario(nuevo_usuario):
        messagebox.showinfo("Registro Exitoso", "¡Usuario registrado correctamente! Ahora puedes iniciar sesión.")
        cambiar_vista(login_frame)
        # Limpiar campos después del registro
        for etiqueta_text, placeholder, is_password in campos_registro:
            cleaned_key = reg_field_keys.get(etiqueta_text, etiqueta_text.lower().replace(":", "").replace(" ", "_"))
            
            # Check if the key exists before attempting to clear/insert placeholder
            if cleaned_key in reg_entries:
                entry = reg_entries[cleaned_key]
                entry.delete(0, tk.END)
                entry.insert(0, placeholder)
                entry.config(fg="gray", show="*" if is_password else "")
    else:
        messagebox.showerror("Error de Registro", "El correo electrónico ya está en uso.")

tk.Button(registro_frame, text="REGISTRAR", bg="#4CAF50", fg="white", width=35, command=registrar).pack(pady=15)
tk.Button(registro_frame, text="¿Ya tienes cuenta? Iniciar Sesión", bg="white", fg="gray", bd=0, font=("Arial", 9), command=lambda: cambiar_vista(login_frame)).pack()


# --- DASHBOARD ---
dashboard_frame = tk.Frame(root, bg=root["bg"]) # Usar el color de fondo de la raíz

# Columna Izquierda del Dashboard
columna_izq = tk.Frame(dashboard_frame, bg="#0d2a52", width=200)
columna_izq.pack(side="left", fill="y")

tk.Label(columna_izq, text="Menú", font=("Arial", 12, "bold"), fg="white", bg="#0d2a52").pack(pady=10)

btn_ver_tareas = tk.Button(columna_izq, text="Ver Tareas", fg="white", bg="#0d2a52",
    font=("Arial", 11, "bold"), bd=0, activebackground="#0d2a52",
    activeforeground="white", cursor="hand2", command=lambda: cambiar_vista(ver_tareas_frame))
btn_ver_tareas.pack(anchor="w", padx=15, pady=5)

btn_crear_tarea_dashboard = tk.Button(columna_izq, text="Crear Tarea", fg="white", bg="#0d2a52", font=("Arial", 11, "bold"), bd=0,
          activebackground="#0d2a52", activeforeground="white", cursor="hand2",
          command=lambda: cambiar_vista(crear_tarea_frame))
btn_crear_tarea_dashboard.pack(anchor="w", padx=15, pady=5)

# Separador
separator_left = tk.Frame(dashboard_frame, bg="white", width=2)
separator_left.pack(side="left", fill="y")

# Columna Central del Dashboard
columna_central = tk.Frame(dashboard_frame, bg="black")
columna_central.pack(side="left", fill="both", expand=True)

botones_superiores_frame = tk.Frame(columna_central, bg="black")
botones_superiores_frame.pack(pady=10)

tk.Button(botones_superiores_frame, text="Nueva tarea ⊕", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
          command=lambda: cambiar_vista(crear_tarea_frame)).pack(side="left", padx=10)

tk.Button(botones_superiores_frame, text="Ordenar por Fecha de Vencimiento ☰", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
          command=lambda: ordenar_tareas_por_fecha()).pack(side="left", padx=10)


scroll_frame_dashboard = tk.Frame(columna_central, bg="black")
scroll_frame_dashboard.pack(fill="both", expand=True)

canvas_tareas_dashboard = tk.Canvas(scroll_frame_dashboard, bg="black", highlightthickness=0)
scrollbar_dashboard = tk.Scrollbar(scroll_frame_dashboard, orient="vertical", command=canvas_tareas_dashboard.yview)
canvas_tareas_dashboard.configure(yscrollcommand=scrollbar_dashboard.set)

scrollbar_dashboard.pack(side="right", fill="y")
canvas_tareas_dashboard.pack(side="left", fill="both", expand=True)

frame_tareas_dashboard = tk.Frame(canvas_tareas_dashboard, bg="black")
# Added tag for the window to fix itemconfigure error
canvas_tareas_dashboard.create_window((0, 0), window=frame_tareas_dashboard, anchor="nw", tags="frame_tareas_dashboard_window")

def on_frame_configure_dashboard(event):
    canvas_tareas_dashboard.configure(scrollregion=canvas_tareas_dashboard.bbox("all"))

def resize_canvas_dashboard(event):
    # Fixed itemconfigure call to use the specific tag of the window
    canvas_tareas_dashboard.itemconfig("frame_tareas_dashboard_window", width=event.width)

def _on_mousewheel_dashboard(event):
    canvas_tareas_dashboard.yview_scroll(int(-1 * (event.delta / 60)), "units")

frame_tareas_dashboard.bind("<Configure>", on_frame_configure_dashboard)
canvas_tareas_dashboard.bind("<Configure>", resize_canvas_dashboard)
canvas_tareas_dashboard.bind("<Enter>", lambda e: canvas_tareas_dashboard.bind_all("<MouseWheel>", _on_mousewheel_dashboard))
canvas_tareas_dashboard.bind("<Leave>", lambda e: canvas_tareas_dashboard.unbind_all("<MouseWheel>"))


# Separador
separator_right = tk.Frame(dashboard_frame, bg="white", width=2)
separator_right.pack(side="left", fill="y")

# Columna Derecha del Dashboard
columna_derecha = tk.Frame(dashboard_frame, bg="#0d2a52", width=220)
columna_derecha.pack(side="right", fill="y")
columna_derecha.pack_propagate(False) # Evita que el frame se ajuste al contenido
tk.Label(columna_derecha, text="Tareas a Vencer", font=("Arial", 11, "bold"), fg="white", bg="#0d2a52").pack(pady=10)


def actualizar_dashboard():
    """Actualiza la lista de tareas en el dashboard."""
    if usuario_actual is None:
        return # No hay usuario logueado

    # Limpiar frames antes de volver a dibujar
    for widget in frame_tareas_dashboard.winfo_children():
        widget.destroy()
    for widget in columna_derecha.winfo_children():
        widget.destroy()

    tk.Label(columna_derecha, text="Tareas a Vencer", font=("Arial", 11, "bold"), fg="white", bg="#0d2a52").pack(pady=10)

    # Obtener tareas del usuario actual desde la base de datos
    global tareas_creadas
    tareas_db = tarea_service.listar_por_usuario(usuario_actual.id)
    print(f"Tareas fetched from DB for dashboard: {len(tareas_db)}") # Debugging print
    # Convertir las tareas de SQLAlchemy a un formato de diccionario para la UI
    tareas_creadas = []
    for t_db in tareas_db:
        subtareas_list = []
        if t_db.subtareas:
            for sub_db in t_db.subtareas:
                # Convertir el booleano de la DB a boolean de Python
                subtareas_list.append({"titulo": sub_db.titulo, "completada": sub_db.completada})

        # Convertir estado booleano de DB a string para la UI
        estado_ui = "Completada" if t_db.estado else "Pendiente"
        # Asegurar que prioridad esté en el formato esperado por la UI
        # CORRECTED: Access .value of Enum before .upper()
        prioridad_ui = t_db.prioridad.value.upper() if t_db.prioridad else "MEDIA" 

        tareas_creadas.append({
            "id": str(t_db.tarea_id), # Usar tarea_id de la DB
            "titulo": t_db.titulo,
            "fecha": t_db.fecha_limite.strftime("%d/%m/%Y"), # Formato esperado por UI
            "estado": estado_ui,
            "prioridad": prioridad_ui,
            "etiqueta": ", ".join([e.nombre for e in t_db.etiquetas]) if t_db.etiquetas else "", # CORREGIDO: Manejo de etiquetas
            "descripcion": t_db.descripcion,
            "subtareas": subtareas_list
        })
    print(f"Tasks to display in dashboard: {len(tareas_creadas)}") # Debugging print

    tk.Label(frame_tareas_dashboard, text="TAREAS PENDIENTES", font=("Arial", 13, "bold"), fg="white", bg="black").pack(pady=10)

    for i, tarea in enumerate(tareas_creadas):
        crear_contenedor_tareas(frame_tareas_dashboard, tarea, i)
        crear_tarea_derecha(tarea)

    canvas_tareas_dashboard.update_idletasks()
    canvas_tareas_dashboard.configure(scrollregion=canvas_tareas_dashboard.bbox("all"))

def crear_contenedor_tareas(master, tarea, index):
    """Crea un contenedor visual para cada tarea en el dashboard."""
    contenedor = tk.Frame(master, bg="#4f4f4f", padx=10, pady=10)
    contenedor.pack(pady=15, padx=20, fill="x")

    info = [
        ("TAREA:", tarea["titulo"]),
        ("Fecha de Límite:", tarea["fecha"]),
        ("Estado:", tarea["estado"]),
        ("Prioridad:", tarea["prioridad"]),
        ("Etiqueta:", tarea["etiqueta"])
    ]

    for etiq, val in info:
        frame = tk.Frame(contenedor, bg="#4f4f4f")
        frame.pack(anchor="w", pady=1, padx=15)
        tk.Label(frame, text=etiq, fg="white", bg="#4f4f4f", font=("Arial", 10, "bold")).pack(side="left")
        tk.Label(frame, text=val, fg="white", bg="#4f4f4f", font=("Arial", 10)).pack(side="left")

    # Subtareas
    tk.Label(contenedor, text="Subtareas:", font=("Arial", 10, "bold"), fg="white", bg="#4f4f4f").pack(anchor="w", padx=15)
    subtareas = tarea.get("subtareas", [])
    completadas = 0
    if subtareas:
        for i, subt in enumerate(subtareas, 1):
            estado_check = "☑" if subt["completada"] else "☐"
            if subt["completada"]:
                completadas += 1
            texto = f"{estado_check} Subtarea {i}: {subt['titulo']}"
            tk.Label(contenedor, text=texto, font=("Arial", 10), fg="white", bg="#4f4f4f").pack(anchor="w", padx=30)
    else:
        tk.Label(contenedor, text="(No hay subtareas)", font=("Arial", 10, "italic"), fg="white", bg="#4f4f4f").pack(anchor="w", padx=30)

    # Descripción
    tk.Label(contenedor, text="Descripción:", font=("Arial", 10, "bold"), fg="white", bg="#4f4f4f", anchor="w").pack(anchor="w", padx=15)
    desc_frame = tk.Frame(contenedor, bg="white", padx=5, pady=5)
    desc_frame.pack(padx=15, fill="x")
    tk.Message(desc_frame, text=tarea["descripcion"], bg="white", width=380, font=("Arial", 10)).pack(anchor="w", pady=(0, 5))

    # Progreso de subtareas
    total = len(subtareas)
    canvas_width = 200
    progress_canvas = tk.Canvas(contenedor, width=canvas_width, height=15, bg="#4f4f4f", highlightthickness=0)
    progress_canvas.pack(pady=5, anchor="w", padx=15)

    if total > 0:
        porcentaje = int((completadas / total) * canvas_width)
        progress_canvas.create_rectangle(0, 0, porcentaje, 15, fill="#4CAF50", width=0)
    else:
        # Si no hay subtareas, barra completa o vacía según el estado de la tarea principal
        if tarea["estado"].lower() == "completada":
            progress_canvas.create_rectangle(0, 0, canvas_width, 15, fill="#4CAF50", width=0)
        else:
            progress_canvas.create_rectangle(0, 0, 0, 15, fill="#4CAF50", width=0)


    # Botones de acción
    tk.Button(contenedor, text="Editar tarea ✎", bg="#1976D2", fg="white", width=15,
              command=lambda: editar_tarea_desde_dashboard(index)).pack(anchor="e", pady=(5, 2), padx=10)

    tk.Button(contenedor, text="Eliminar tarea 🗑", bg="#D32F2F", fg="white", width=15,
              command=lambda: eliminar_tarea(index)).pack(anchor="e", pady=(0, 5), padx=10)

    if tarea["estado"].lower() != "completada":
        tk.Button(contenedor, text="✔ Marcar como completada", bg="#4CAF50", fg="white", width=20,
                  command=lambda: marcar_como_completada(index)).pack(anchor="e", pady=(5, 2), padx=10)


def crear_tarea_derecha(tarea):
    """Crea un widget de tarea para la columna 'Tareas a Vencer'."""
    try:
        fecha_limite = datetime.strptime(tarea["fecha"], "%d/%m/%Y")
    except ValueError:
        return # Ignorar si la fecha es inválida

    hoy = datetime.today()
    # Solo mostrar si la tarea no está completada y no ha vencido (o vence hoy)
    # CORRECTED: Access .date() of datetime.datetime for comparison
    if not (tarea["estado"].lower() == "completada") and fecha_limite.date() >= hoy.date():
        tarea_frame = tk.Frame(columna_derecha, bg="#1a4d7d", relief="solid", bd=1) # Un azul más oscuro
        tarea_frame.pack(pady=5, padx=10, fill="x")
        tarea_label = tk.Label(
            tarea_frame,
            text=f"TAREA: {tarea['titulo']}\nVence: {tarea['fecha']}",
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#1a4d7d",
            padx=10,
            pady=5,
            justify="left"
        )
        tarea_label.pack(fill="x")

def ordenar_tareas_por_fecha():
    """Ordena las tareas mostradas por fecha de vencimiento."""
    def fecha_a_datetime(tarea):
        try:
            return datetime.strptime(tarea["fecha"], "%d/%m/%Y")
        except ValueError:
            return datetime.max # Si la fecha es inválida, la manda al final

    tareas_creadas.sort(key=fecha_a_datetime)
    actualizar_dashboard() # Re-renderiza las tareas ordenadas


def eliminar_tarea(index):
    """Elimina una tarea de la base de datos y actualiza la UI."""
    if 0 <= index < len(tareas_creadas):
        tarea_id = tareas_creadas[index]["id"] # Usar 'id' que viene de 'tarea_id' de la DB
        if messagebox.askyesno("Confirmar Eliminación", "¿Estás seguro de que quieres eliminar esta tarea?"):
            if tarea_service.eliminar_tarea(tarea_id):
                messagebox.showinfo("Tarea Eliminada", "La tarea ha sido eliminada exitosamente.")
                actualizar_dashboard()
            else:
                messagebox.showerror("Error", "No se pudo eliminar la tarea.")


def marcar_como_completada(index):
    """Marca una tarea como completada en la base de datos y actualiza la UI."""
    if 0 <= index < len(tareas_creadas):
        tarea_id = tareas_creadas[index]["id"] # Usar 'id' que viene de 'tarea_id' de la DB
        # Convertir a booleano para la DB
        if tarea_service.actualizar_estado_tarea(tarea_id, True): # True para 'Completada'
            messagebox.showinfo("Tarea Completada", "La tarea ha sido marcada como completada.")
            actualizar_dashboard()
        else:
            messagebox.showerror("Error", "No se pudo marcar la tarea como completada.")


def editar_tarea_desde_dashboard(index):
    """Prepara el formulario de edición con los datos de la tarea seleccionada."""
    global tarea_index_actual, tarea_actual_data # Renombre para evitar conflicto con la clase Tarea
    tarea_index_actual = index
    tarea_actual_data = tareas_creadas[tarea_index_actual] # Datos de la tarea seleccionada

    cambiar_vista(editar_tarea_frame)

    # Limpiar campos de edición antes de rellenar
    entry_editar_titulo.delete(0, tk.END)
    entry_editar_fecha.delete(0, tk.END)
    entry_editar_etiqueta.delete(0, tk.END)
    text_editar_descripcion.delete("1.0", tk.END)

    # Rellenar campos con los datos de la tarea actual
    entry_editar_titulo.insert(0, tarea_actual_data["titulo"])
    entry_editar_fecha.insert(0, tarea_actual_data["fecha"])
    # Set OptionMenu values
    var_editar_estado.set(tarea_actual_data["estado"])
    var_editar_prioridad.set(tarea_actual_data["prioridad"])
    
    entry_editar_etiqueta.insert(0, tk.END) # Clear it first
    entry_editar_etiqueta.insert(0, tarea_actual_data["etiqueta"])
    text_editar_descripcion.delete("1.0", tk.END) # Clear it first
    text_editar_descripcion.insert("1.0", tarea_actual_data["descripcion"])

    # Limpiar y cargar subtareas en la interfaz de edición
    for ent, var, frame in subtarea_widgets_editar:
        frame.destroy()
    subtarea_widgets_editar.clear()

    for subt in tarea_actual_data.get("subtareas", []):
        agregar_subtarea_widget_editar(subt["titulo"], subt["completada"])

    if not tarea_actual_data.get("subtareas", []):
        agregar_subtarea_widget_editar() # Agrega al menos una subtarea vacía


# --- CREAR TAREA ---
crear_tarea_frame = tk.Frame(root, bg="white")

canvas_crear = tk.Canvas(crear_tarea_frame, bg="white", highlightthickness=0)
scrollbar_crear = tk.Scrollbar(crear_tarea_frame, orient="vertical", command=canvas_crear.yview)
canvas_crear.configure(yscrollcommand=scrollbar_crear.set)

scrollbar_crear.pack(side="right", fill="y")
canvas_crear.pack(side="left", fill="both", expand=True)

frame_crear_scroll = tk.Frame(canvas_crear, bg="white")
canvas_crear.create_window((0, 0), window=frame_crear_scroll, anchor="nw", tags="frame_crear_scroll_window")

def on_frame_configure_crear(event):
    canvas_crear.configure(scrollregion=canvas_crear.bbox("all"))
def resize_canvas_crear(event):
    canvas_crear.itemconfig("frame_crear_scroll_window", width=event.width)
def _on_mousewheel_crear(event):
    canvas_crear.yview_scroll(int(-1 * (event.delta / 60)), "units")

frame_crear_scroll.bind("<Configure>", on_frame_configure_crear)
canvas_crear.bind("<Configure>", resize_canvas_crear)
canvas_crear.bind("<Enter>", lambda e: canvas_crear.bind_all("<MouseWheel>", _on_mousewheel_crear))
canvas_crear.bind("<Leave>", lambda e: canvas_crear.unbind_all("<MouseWheel>"))

# Campos del formulario de Crear Tarea
tk.Label(frame_crear_scroll, text="Título de la Tarea:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_crear_titulo = tk.Entry(frame_crear_scroll, width=50)
entry_crear_titulo.pack(padx=70, pady=5)

tk.Label(frame_crear_scroll, text="Fecha Límite (dd/mm/aaaa):", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_crear_fecha = tk.Entry(frame_crear_scroll, width=50)
entry_crear_fecha.pack(padx=70, pady=5)

# Dropdown para Estado en Crear Tarea
tk.Label(frame_crear_scroll, text="Estado:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
opciones_estado = ["Pendiente", "Completada"]
var_crear_estado = tk.StringVar(root)
var_crear_estado.set(opciones_estado[0]) # Valor por defecto
tk.OptionMenu(frame_crear_scroll, var_crear_estado, *opciones_estado).pack(padx=70, pady=5, anchor="w")

# Dropdown para Prioridad en Crear Tarea
tk.Label(frame_crear_scroll, text="Prioridad:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
opciones_prioridad = [p.value for p in PrioridadEnum] # Obtener valores de la enumeración
var_crear_prioridad = tk.StringVar(root)
var_crear_prioridad.set(PrioridadEnum.MEDIA.value) # Valor por defecto
tk.OptionMenu(frame_crear_scroll, var_crear_prioridad, *opciones_prioridad).pack(padx=70, pady=5, anchor="w")

tk.Label(frame_crear_scroll, text="Etiqueta:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_crear_etiqueta = tk.Entry(frame_crear_scroll, width=50)
entry_crear_etiqueta.pack(padx=70, pady=5)

# Subtareas para Crear Tarea
tk.Label(frame_crear_scroll, text="Subtareas:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=70, pady=(10, 0))

subtareas_entries = [] # Lista para guardar entradas de subtareas de la vista crear
subtareas_container_crear = tk.Frame(frame_crear_scroll, bg="white")
subtareas_container_crear.pack(anchor="w", padx=70, pady=5)

def agregar_subtarea_crear():
    entry = tk.Entry(subtareas_container_crear, font=("Arial", 10), width=40)
    entry.pack(pady=2, anchor="w")
    subtareas_entries.append(entry)

def eliminar_ultima_subtarea_crear():
    if subtareas_entries:
        ultima = subtareas_entries.pop()
        ultima.destroy()

botones_subtarea_frame_crear = tk.Frame(frame_crear_scroll, bg="white")
botones_subtarea_frame_crear.pack(anchor="w", padx=70, pady=5)

tk.Button(botones_subtarea_frame_crear, text="➕ Añadir Subtarea", bg="#4CAF50", fg="white",
          font=("Arial", 10), command=agregar_subtarea_crear).pack(side="left", padx=(0, 10))

tk.Button(botones_subtarea_frame_crear, text="🗑️ Eliminar Subtarea", bg="#f44336", fg="white",
          font=("Arial", 10), command=eliminar_ultima_subtarea_crear).pack(side="left")

# Descripción para Crear Tarea
tk.Label(frame_crear_scroll, text="Descripción:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
text_crear_descripcion = tk.Text(frame_crear_scroll, width=50, height=4)
text_crear_descripcion.pack(padx=70, pady=5)

def guardar_nueva_tarea():
    """Guarda una nueva tarea en la base de datos."""
    if usuario_actual is None:
        messagebox.showerror("Error", "Debes iniciar sesión para crear tareas.")
        return

    titulo = entry_crear_titulo.get().strip()
    fecha_str = entry_crear_fecha.get().strip()
    estado_ui = var_crear_estado.get() # Obtener del OptionMenu
    prioridad_ui = var_crear_prioridad.get() # Obtener del OptionMenu
    etiqueta = entry_crear_etiqueta.get().strip()
    descripcion = text_crear_descripcion.get("1.0", tk.END).strip()

    if not all([titulo, fecha_str, estado_ui, prioridad_ui, etiqueta, descripcion]):
        messagebox.showwarning("Error", "Por favor, completa todos los campos.")
        return

    _, err_fecha = validar_fecha(fecha_str)
    if err_fecha:
        messagebox.showerror("Error de Fecha", err_fecha)
        return

    try:
        fecha_limite_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Error de Fecha", "Formato de fecha inválido. Usa dd/mm/aaaa.")
        return

    # Convertir estado de UI a booleano para la DB
    estado_db = True if estado_ui.lower() == "completada" else False

    # Recoger subtareas
    subtareas_data = []
    for entry in subtareas_entries:
        subtarea_titulo = entry.get().strip()
        if subtarea_titulo:
            subtareas_data.append({"titulo": subtarea_titulo, "completada": False})

    nueva_tarea = Tarea(
        tarea_id=str(uuid.uuid4()), # Usar tarea_id como PRIMARY KEY
        usuario_id=usuario_actual.id, # Pasa el ID del usuario directamente
        titulo=titulo,
        fecha_creacion=datetime.now(), # Asignar fecha de creación
        fecha_limite=fecha_limite_obj,
        estado=estado_db, # Usar el booleano para la DB
        prioridad=PrioridadEnum[prioridad_ui], # Convertir a Enum directamente para el modelo
        categoria_id=None, # Asumo que no estás usando categorías en la UI de creación aún
        # No se pasa `etiqueta` directamente al constructor de Tarea
        descripcion=descripcion
    )

    # El servicio de tarea debe manejar la creación/vinculación de etiquetas
    if tarea_service.crear_tarea(nueva_tarea, subtareas_data, etiquetas_str=etiqueta):
        messagebox.showinfo("Tarea Creada", "La tarea ha sido creada exitosamente.")
        cambiar_vista(dashboard_frame) # Volver al dashboard
    else:
        messagebox.showerror("Error", "No se pudo crear la tarea.")

tk.Button(frame_crear_scroll, text="GUARDAR TAREA", bg="#4CAF50", fg="white", width=35, command=guardar_nueva_tarea).pack(pady=10)
tk.Button(frame_crear_scroll, text="CANCELAR", bg="#f44336", fg="white", width=35, command=lambda: cambiar_vista(dashboard_frame)).pack(pady=(0, 20))


# --- EDITAR TAREA ---
editar_tarea_frame = tk.Frame(root, bg="white")

canvas_editar = tk.Canvas(editar_tarea_frame, bg="white", highlightthickness=0)
scrollbar_editar = tk.Scrollbar(editar_tarea_frame, orient="vertical", command=canvas_editar.yview)
canvas_editar.configure(yscrollcommand=scrollbar_editar.set)

scrollbar_editar.pack(side="right", fill="y")
canvas_editar.pack(side="left", fill="both", expand=True)

frame_editar_scroll = tk.Frame(canvas_editar, bg="white", width=430)
canvas_editar.create_window((0, 0), window=frame_editar_scroll, anchor="nw", tags="frame_editar_scroll_window")

def configurar_scroll_editar(event):
    canvas_editar.configure(scrollregion=canvas_editar.bbox("all"))
    canvas_editar.itemconfig("frame_editar_scroll_window", width=event.width)
def _on_mousewheel_editar(event):
    canvas_editar.yview_scroll(int(-1*(event.delta/60)), "units")

frame_editar_scroll.bind("<Configure>", configurar_scroll_editar)
canvas_editar.bind("<Enter>", lambda e: canvas_editar.bind_all("<MouseWheel>", _on_mousewheel_editar))
canvas_editar.bind("<Leave>", lambda e: canvas_editar.unbind_all("<MouseWheel>"))

# Campos del formulario de Editar Tarea
tk.Label(frame_editar_scroll, text="Título de la Tarea:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_editar_titulo = tk.Entry(frame_editar_scroll, width=50, fg="black", font=("Arial", 10))
entry_editar_titulo.pack(padx=70, pady=5)

tk.Label(frame_editar_scroll, text="Fecha Límite (dd/mm/aaaa):", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_editar_fecha = tk.Entry(frame_editar_scroll, width=50, fg="black", font=("Arial", 10))
entry_editar_fecha.pack(padx=70, pady=5)

# Dropdown para Estado en Editar Tarea
tk.Label(frame_editar_scroll, text="Estado:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
var_editar_estado = tk.StringVar(root)
var_editar_estado.set(opciones_estado[0]) # Valor por defecto
tk.OptionMenu(frame_editar_scroll, var_editar_estado, *opciones_estado).pack(padx=70, pady=5, anchor="w")

# Dropdown para Prioridad en Editar Tarea
tk.Label(frame_editar_scroll, text="Prioridad:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
var_editar_prioridad = tk.StringVar(root)
var_editar_prioridad.set(PrioridadEnum.MEDIA.value) # Valor por defecto
tk.OptionMenu(frame_editar_scroll, var_editar_prioridad, *opciones_prioridad).pack(padx=70, pady=5, anchor="w")

tk.Label(frame_editar_scroll, text="Etiqueta:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
entry_editar_etiqueta = tk.Entry(frame_editar_scroll, width=50, fg="black", font=("Arial", 10))
entry_editar_etiqueta.pack(padx=70, pady=5)

# Subtareas para Editar Tarea
tk.Label(frame_editar_scroll, text="Subtareas:", font=("Arial", 10, "bold"), bg="white").pack(anchor="w", padx=70, pady=(10, 0))

subtareas_container_editar = tk.Frame(frame_editar_scroll, bg="white")
subtareas_container_editar.pack(anchor="w", padx=70, pady=5)

def agregar_subtarea_widget_editar(titulo="", completada=False):
    frame_subtarea = tk.Frame(subtareas_container_editar, bg="white")
    frame_subtarea.pack(anchor="w", pady=2)

    var = tk.BooleanVar(value=completada)
    chk = tk.Checkbutton(frame_subtarea, variable=var, bg="white")
    chk.pack(side="left")

    ent = tk.Entry(frame_subtarea, width=35, font=("Arial", 10))
    ent.insert(0, titulo)
    ent.pack(side="left", padx=5)

    subtarea_widgets_editar.append((ent, var, frame_subtarea))

def eliminar_ultima_subtarea_editar():
    if subtarea_widgets_editar:
        entry, var, frame = subtarea_widgets_editar.pop()
        frame.destroy()

botones_subtarea_frame_editar = tk.Frame(frame_editar_scroll, bg="white")
botones_subtarea_frame_editar.pack(anchor="w", padx=70, pady=5)

tk.Button(botones_subtarea_frame_editar, text="➕ Añadir Subtarea", bg="#4CAF50", fg="white",
          font=("Arial", 10), command=agregar_subtarea_widget_editar).pack(side="left", padx=(0, 10))

tk.Button(botones_subtarea_frame_editar, text="🗑️ Eliminar Subtarea", bg="#f44336", fg="white",
          font=("Arial", 10), command=eliminar_ultima_subtarea_editar).pack(side="left")


# Descripción para Editar Tarea
tk.Label(frame_editar_scroll, text="Descripción:", font=("Arial", 10), bg="white").pack(anchor="w", padx=70, pady=(10, 0))
text_editar_descripcion = tk.Text(frame_editar_scroll, width=50, height=4, wrap="word", fg="black", font=("Arial", 10))
text_editar_descripcion.pack(padx=70, pady=5)

def guardar_cambios_tarea_actualizada():
    """Guarda los cambios de una tarea editada en la base de datos."""
    global tarea_index_actual
    if usuario_actual is None or tarea_index_actual is None:
        messagebox.showerror("Error", "No hay tarea seleccionada para editar o no has iniciado sesión.")
        return

    tarea_id = tareas_creadas[tarea_index_actual]["id"] # Usar 'id' que es 'tarea_id' de la DB
    titulo = entry_editar_titulo.get().strip()
    fecha_str = entry_editar_fecha.get().strip()
    estado_ui = var_editar_estado.get() # Obtener del OptionMenu
    prioridad_ui = var_editar_prioridad.get() # Obtener del OptionMenu
    etiqueta = entry_editar_etiqueta.get().strip()
    descripcion = text_editar_descripcion.get("1.0", tk.END).strip()

    if not all([titulo, fecha_str, estado_ui, prioridad_ui, etiqueta, descripcion]):
        messagebox.showwarning("Error", "Por favor, completa todos los campos.")
        return

    _, err_fecha = validar_fecha(fecha_str)
    if err_fecha:
        messagebox.showerror("Error de Fecha", err_fecha)
        return

    try:
        fecha_limite_obj = datetime.strptime(fecha_str, "%d/%m/%Y").date()
    except ValueError:
        messagebox.showerror("Error de Fecha", "Formato de fecha inválido. Usa dd/mm/aaaa.")
        return

    # Convertir estado de UI a booleano para la DB
    estado_db = True if estado_ui.lower() == "completada" else False

    # Recoger subtareas actualizadas
    subtareas_actualizadas = []
    for ent, var, frame in subtarea_widgets_editar:
        subtarea_titulo = ent.get().strip()
        if subtarea_titulo:
            subtareas_actualizadas.append({"titulo": subtarea_titulo, "completada": var.get()})

    # Crear un diccionario con los datos a actualizar
    datos_a_actualizar = {
        "titulo": titulo,
        "fecha_limite": fecha_limite_obj,
        "estado": estado_db, # Usar el booleano para la DB
        "prioridad": PrioridadEnum[prioridad_ui], # Convertir a Enum directamente para el modelo
        # "etiqueta": etiqueta, # `etiqueta` no es un campo directo en el modelo Tarea
        "descripcion": descripcion,
        # "categoria_id": ... Si estuvieras manejando esto en la UI
    }

    # Llamar al servicio de tarea. Asumo que el servicio ahora maneja la actualización de subtareas y etiquetas
    if tarea_service.actualizar_tarea_con_subtareas(tarea_id, datos_a_actualizar, subtareas_actualizadas, etiquetas_str=etiqueta):
        messagebox.showinfo("Tarea Editada", "La tarea ha sido actualizada correctamente.")
        cambiar_vista(dashboard_frame) # Volver al dashboard
    else:
        messagebox.showerror("Error", "No se pudo actualizar la tarea.")


tk.Button(frame_editar_scroll, text="GUARDAR CAMBIOS", bg="#4CAF50", fg="white", width=35, command=guardar_cambios_tarea_actualizada).pack(pady=10)
tk.Button(frame_editar_scroll, text="CANCELAR", bg="#f44336", fg="white", width=35, command=lambda: cambiar_vista(dashboard_frame)).pack(pady=(0, 20))


# --- VER TAREAS (Duplicado del dashboard para filtro) ---
ver_tareas_frame = tk.Frame(root, bg=root["bg"])

# Declarar marcos principales de la sección "Ver Tareas" como globales
global columna_izq_ver, separator_left_ver, columna_central_ver, \
       botones_filtro_frame_ver, scroll_frame_ver, canvas_tareas_ver, \
       scrollbar_ver, frame_tareas_ver, separator_right_ver, columna_derecha_ver


columna_izq_ver = tk.Frame(ver_tareas_frame, bg="#0d2a52", width=200)
columna_izq_ver.pack(side="left", fill="y")

tk.Label(columna_izq_ver, text="Menú", font=("Arial", 12, "bold"), fg="white", bg="#0d2a52").pack(pady=10)

btn_ver_tareas_ver = tk.Button(columna_izq_ver, text="Ver Tareas", fg="white", bg="#0d2a52",
    font=("Arial", 11, "bold"), bd=0, activebackground="#0d2a52",
    activeforeground="white", cursor="hand2", command=lambda: cambiar_vista(ver_tareas_frame))
btn_ver_tareas_ver.pack(anchor="w", padx=15, pady=5)

btn_crear_tarea_ver = tk.Button(columna_izq_ver, text="Crear Tarea", fg="white", bg="#0d2a52",
    font=("Arial", 11, "bold"), bd=0, activebackground="#0d2a52",
    activeforeground="white", cursor="hand2", command=lambda: cambiar_vista(crear_tarea_frame))
btn_crear_tarea_ver.pack(anchor="w", padx=15, pady=5)


separator_left_ver = tk.Frame(ver_tareas_frame, bg="white", width=2)
separator_left_ver.pack(side="left", fill="y")

columna_central_ver = tk.Frame(ver_tareas_frame, bg="black")
columna_central_ver.pack(side="left", fill="both", expand=True)

botones_filtro_frame_ver = tk.Frame(columna_central_ver, bg="black")
botones_filtro_frame_ver.pack(pady=10)

btn_todas = tk.Button(botones_filtro_frame_ver, text="Todas las tareas", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                      command=lambda: actualizar_tareas_ver()) # Usa la función de actualización sin filtros
btn_todas.pack(side="left", padx=10)

btn_vencidas = tk.Button(botones_filtro_frame_ver, text="Tareas vencidas", bg="#FF5722", fg="white", font=("Arial", 10, "bold"), # Naranja para vencidas
                         command=lambda: mostrar_tareas_filtradas_ver("Vencidas"))
btn_vencidas.pack(side="left", padx=10)

btn_completadas = tk.Button(botones_filtro_frame_ver, text="Tareas completadas", bg="#2196F3", fg="white", font=("Arial", 10, "bold"), # Azul para completadas
                            command=lambda: mostrar_tareas_filtradas_ver("Completadas"))
btn_completadas.pack(side="left", padx=10)

scroll_frame_ver = tk.Frame(columna_central_ver, bg="black")
scroll_frame_ver.pack(fill="both", expand=True)

canvas_tareas_ver = tk.Canvas(scroll_frame_ver, bg="black", highlightthickness=0)
scrollbar_ver = tk.Scrollbar(scroll_frame_ver, orient="vertical", command=canvas_tareas_ver.yview)
canvas_tareas_ver.configure(yscrollcommand=scrollbar_ver.set)

scrollbar_ver.pack(side="right", fill="y")
canvas_tareas_ver.pack(side="left", fill="both", expand=True)

frame_tareas_ver = tk.Frame(canvas_tareas_ver, bg="black")
canvas_tareas_ver.create_window((0, 0), window=frame_tareas_ver, anchor="nw", tags="frame_tareas_ver_window")

def on_frame_configure_ver(event):
    canvas_tareas_ver.configure(scrollregion=canvas_tareas_ver.bbox("all"))

def resize_canvas_ver(event):
    canvas_tareas_ver.itemconfig("frame_tareas_ver_window", width=event.width)

def _on_mousewheel_ver(event):
    canvas_tareas_ver.yview_scroll(int(-1 * (event.delta / 60)), "units")

frame_tareas_ver.bind("<Configure>", on_frame_configure_ver)
canvas_tareas_ver.bind("<Configure>", resize_canvas_ver)
canvas_tareas_ver.bind("<Enter>", lambda e: canvas_tareas_ver.bind_all("<MouseWheel>", _on_mousewheel_ver))
canvas_tareas_ver.bind("<Leave>", lambda e: canvas_tareas_ver.unbind_all("<MouseWheel>"))


separator_right_ver = tk.Frame(ver_tareas_frame, bg="white", width=2)
separator_right_ver.pack(side="left", fill="y")

columna_derecha_ver = tk.Frame(ver_tareas_frame, bg="#0d2a52", width=220)
columna_derecha_ver.pack(side="right", fill="y")
columna_derecha_ver.pack_propagate(False)
tk.Label(columna_derecha_ver, text="Tareas a Vencer", font=("Arial", 11, "bold"), fg="white", bg="#0d2a52").pack(pady=10)


def actualizar_tareas_ver():
    """Actualiza la vista de tareas en la pantalla 'Ver Tareas'."""
    if usuario_actual is None:
        return

    for widget in frame_tareas_ver.winfo_children():
        widget.destroy()
    for widget in columna_derecha_ver.winfo_children():
        widget.destroy()

    tk.Label(columna_derecha_ver, text="Tareas a Vencer", font=("Arial", 11, "bold"), fg="white", bg="#0d2a52").pack(pady=10)

    global tareas_creadas
    tareas_db = tarea_service.listar_por_usuario(usuario_actual.id)
    print(f"Tareas fetched from DB for 'Ver Tareas': {len(tareas_db)}") # Debugging print
    tareas_creadas = [] # Reinicia la lista global para esta vista

    for t_db in tareas_db:
        subtareas_list = []
        if t_db.subtareas:
            for sub_db in t_db.subtareas:
                subtareas_list.append({"titulo": sub_db.titulo, "completada": sub_db.completada})

        estado_ui = "Completada" if t_db.estado else "Pendiente"
        # CORRECTED: Access .value of Enum before .upper()
        prioridad_ui = t_db.prioridad.value.upper() if t_db.prioridad else "MEDIA"

        tareas_creadas.append({
            "id": str(t_db.tarea_id), # Usar tarea_id de la DB
            "titulo": t_db.titulo,
            "fecha": t_db.fecha_limite.strftime("%d/%m/%Y"),
            "estado": estado_ui,
            "prioridad": prioridad_ui,
            "etiqueta": ", ".join([e.nombre for e in t_db.etiquetas]) if t_db.etiquetas else "", # CORREGIDO: Manejo de etiquetas
            "descripcion": t_db.descripcion,
            "subtareas": subtareas_list
        })
    print(f"Tasks to display in 'Ver Tareas': {len(tareas_creadas)}") # Debugging print


    # Ordenar por fecha por defecto
    tareas_creadas.sort(key=lambda t: datetime.strptime(t["fecha"], "%d/%m/%Y") if isinstance(t["fecha"], str) else datetime.max)


    tk.Label(frame_tareas_ver, text="TAREAS PENDIENTES", font=("Arial", 13, "bold"), fg="white", bg="black").pack(pady=10) # Cambio de filtro_tipo.upper() a "PENDIENTES"

    for i, tarea in enumerate(tareas_creadas):
        crear_contenedor_tareas(frame_tareas_ver, tarea, i) # Reutiliza la función del dashboard
        crear_tarea_derecha_ver(tarea)

    canvas_tareas_ver.update_idletasks()
    canvas_tareas_ver.configure(scrollregion=canvas_tareas_ver.bbox("all"))


def mostrar_tareas_filtradas_ver(filtro_tipo):
    """Muestra tareas filtradas en la vista 'Ver Tareas'."""
    if usuario_actual is None:
        return

    for widget in frame_tareas_ver.winfo_children():
        widget.destroy()
    for widget in columna_derecha_ver.winfo_children():
        widget.destroy()

    tk.Label(columna_derecha_ver, text="Tareas a Vencer", font=("Arial", 11, "bold"), fg="white", bg="#0d2a52").pack(pady=10)

    filtradas = []
    hoy = datetime.today().date() # Solo la fecha, sin la hora

    if filtro_tipo == "Vencidas":
        tareas_db = tarea_service.listar_por_usuario(usuario_actual.id, estado=None) # Obtener todas las tareas para filtrar por fecha
        for t_db in tareas_db:
            # CORRECTED: Access .date() of datetime.datetime for comparison
            if t_db.fecha_limite and t_db.fecha_limite.date() < hoy: 
                subtareas_list = [{"titulo": sub_db.titulo, "completada": sub_db.completada} for sub_db in t_db.subtareas]
                estado_ui = "Completada" if t_db.estado else "Pendiente"
                prioridad_ui = t_db.prioridad.value.upper() if t_db.prioridad else "MEDIA" # CORRECTED
                filtradas.append({
                    "id": str(t_db.tarea_id),
                    "titulo": t_db.titulo,
                    "fecha": t_db.fecha_limite.strftime("%d/%m/%Y"),
                    "estado": estado_ui,
                    "prioridad": prioridad_ui,
                    "etiqueta": ", ".join([e.nombre for e in t_db.etiquetas]) if t_db.etiquetas else "", # CORREGIDO: Manejo de etiquetas
                    "descripcion": t_db.descripcion,
                    "subtareas": subtareas_list
                })
    elif filtro_tipo == "Completadas":
        # Asegúrate de que listar_por_usuario en TareaService pueda filtrar por estado
        tareas_db = tarea_service.listar_por_usuario(usuario_actual.id, estado=True)
        for t_db in tareas_db:
            subtareas_list = [{"titulo": sub_db.titulo, "completada": sub_db.completada} for sub_db in t_db.subtareas]
            estado_ui = "Completada" if t_db.estado else "Pendiente"
            prioridad_ui = t_db.prioridad.value.upper() if t_db.prioridad else "MEDIA" # CORRECTED
            filtradas.append({
                "id": str(t_db.tarea_id),
                "titulo": t_db.titulo,
                "fecha": t_db.fecha_limite.strftime("%d/%m/%Y"),
                "estado": estado_ui,
                "prioridad": prioridad_ui,
                "etiqueta": ", ".join([e.nombre for e in t_db.etiquetas]) if t_db.etiquetas else "", # CORREGIDO: Manejo de etiquetas
                "descripcion": t_db.descripcion,
                "subtareas": subtareas_list
            })
    else: # "Todas las tareas" o cualquier otro caso por defecto
        # Esto debería ser manejado por un botón "Todas las tareas" que llama a actualizar_tareas_ver() directamente
        # En este contexto, si llegamos aquí, es un filtro no reconocido o un caso que debe comportarse como "Todas"
        # y la etiqueta del título se actualizará cuando se llame a actualizar_tareas_ver()
        pass # No hacer nada aquí, dejar que el flujo principal de 'actualizar_tareas_ver' se encargue

    label_text = ""
    if filtro_tipo == "Vencidas":
        label_text = "TAREAS VENCIDAS"
    elif filtro_tipo == "Completadas":
        label_text = "TAREAS COMPLETADAS"
    else:
        label_text = "TODAS LAS TAREAS" # Esto solo se debería ver si se llama directamente con un filtro no manejado


    tk.Label(frame_tareas_ver, text=label_text, font=("Arial", 13, "bold"), fg="white", bg="black").pack(pady=10)

    for i, tarea in enumerate(filtradas):
        crear_contenedor_tareas(frame_tareas_ver, tarea, i)
        crear_tarea_derecha_ver(tarea) # Muestra en la columna derecha las tareas a vencer (si las hay)

    canvas_tareas_ver.update_idletasks()
    canvas_tareas_ver.configure(scrollregion=canvas_tareas_ver.bbox("all"))

def crear_tarea_derecha_ver(tarea):
    """Crea el contenedor de tareas para la columna derecha de 'Ver Tareas' (solo a vencer)."""
    try:
        fecha_limite = datetime.strptime(tarea["fecha"], "%d/%m/%Y")
    except ValueError:
        return

    # Solo mostrar si la tarea no está completada y no ha vencido (o vence hoy)
    # CORRECTED: Access .date() of datetime.datetime for comparison
    if not (tarea["estado"].lower() == "completada") and fecha_limite.date() >= datetime.today().date():
        tarea_frame = tk.Frame(columna_derecha_ver, bg="#1a4d7d", relief="solid", bd=1)
        tarea_frame.pack(pady=5, padx=10, fill="x")
        tarea_label = tk.Label(
            tarea_frame,
            text=f"TAREA: {tarea['titulo']}\nVence: {tarea['fecha']}",
            font=("Arial", 9, "bold"),
            fg="white",
            bg="#1a4d7d",
            padx=10,
            pady=5,
            justify="left"
        )
        tarea_label.pack(fill="x")


# --- Cerrar Sesión ---
def cerrar_sesion():
    global usuario_actual
    usuario_actual = None
    messagebox.showinfo("Sesión", "Has cerrado sesión.")
    cambiar_vista(login_frame)
    # Limpiar campos de login para el siguiente usuario
    entry_login_correo.delete(0, tk.END)
    entry_login_correo.insert(0, "Ingrese su Correo Electrónico")
    entry_login_correo.config(fg="gray")

    entry_login_pass.delete(0, tk.END)
    entry_login_pass.insert(0, "Ingrese su contraseña")
    entry_login_pass.config(fg="gray", show="")


# --- Inicio de la aplicación ---
cambiar_vista(login_frame) # Iniciar en la pantalla de login
root.mainloop()

# Cerrar la sesión de la base de datos al salir
session.close()
