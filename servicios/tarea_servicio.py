from sqlalchemy.orm import Session
from modelos.tarea import Tarea, PrioridadEnum
from modelos.subtarea import Subtarea # Importa Subtarea
from modelos.etiqueta import Etiqueta # Importa Etiqueta
# Importa las funciones del repositorio de tarea
from repositorios.tarea_repositorio import (
    insertar_tarea,
    obtener_tareas_por_usuario,
    obtener_tarea_por_id,
    actualizar_tarea,
    eliminar_tarea_por_id
)
# Importa las funciones del repositorio de subtarea
from repositorios.subtarea_repositorio import ( # Asegúrate de que las funciones aquí ya estén actualizadas
    insertar_subtarea,
    obtener_subtareas_por_tarea,
    actualizar_subtarea,
    eliminar_subtarea
)
from servicios.etiqueta_servicio import EtiquetaService # Importa EtiquetaService
import uuid # Para generar IDs para subtareas
from datetime import datetime, date # Import necessary for type hints

class TareaService:
    def __init__(self, session: Session):
        self.session = session
        self.etiqueta_service = EtiquetaService(session) # Instancia EtiquetaService

    def crear_tarea(self, tarea: Tarea, subtareas_data: list = None, etiquetas_str: str = "") -> bool:
        """
        Crea una nueva tarea, sus subtareas asociadas y vincula etiquetas.
        :param tarea: Objeto Tarea a crear.
        :param subtareas_data: Lista de diccionarios con datos de subtareas.
        :param etiquetas_str: Cadena de texto con nombres de etiquetas separados por comas.
        :return: True si la tarea se creó exitosamente, False en caso contrario.
        """
        try:
            # Primero inserta la tarea
            insertar_tarea(
                self.session,
                tarea.tarea_id,
                tarea.titulo,
                tarea.descripcion,
                tarea.fecha_creacion,
                tarea.fecha_limite,
                tarea.estado,
                tarea.prioridad,
                tarea.usuario_id,
                tarea.categoria_id,
                etiquetas=None # Las etiquetas se añadirán después
            )
            self.session.flush() # Asegura que la tarea tenga un ID antes de vincular subtareas/etiquetas

            # Manejar subtareas
            if subtareas_data:
                for sub_data in subtareas_data:
                    nueva_subtarea = Subtarea(
                        subtarea_id=str(uuid.uuid4()), # ✅ CORRECCIÓN: Usar 'subtarea_id'
                        titulo=sub_data['titulo'],
                        descripcion=sub_data.get('descripcion', ''), # Asume descripción opcional
                        completada=sub_data.get('completada', False),
                        tarea_id=tarea.tarea_id
                    )
                    insertar_subtarea(self.session, nueva_subtarea.subtarea_id, nueva_subtarea.titulo, # Pasa la sesión, ✅ CORRECCIÓN: usar subtarea_id
                                      nueva_subtarea.descripcion, nueva_subtarea.completada,
                                      nueva_subtarea.tarea_id)
            
            # Manejar etiquetas
            if etiquetas_str:
                nombres_etiquetas = [name.strip() for name in etiquetas_str.split(',') if name.strip()]
                etiquetas_para_tarea = []
                for nombre in nombres_etiquetas:
                    etiqueta_obj = self.etiqueta_service.get_or_create_etiqueta(nombre)
                    etiquetas_para_tarea.append(etiqueta_obj)
                
                # Obtener la tarea recién creada (o ya existente en la sesión) para vincular etiquetas
                tarea_obj = self.session.query(Tarea).filter_by(tarea_id=tarea.tarea_id).first()
                if tarea_obj:
                    tarea_obj.etiquetas.extend(etiquetas_para_tarea)
            
            self.session.commit() # Commit all changes at the service level
            return True
        except Exception as e:
            self.session.rollback() # Rollback on error
            print(f"Error al crear tarea: {e}")
            return False

    def listar_por_usuario(self, usuario_id: str, estado: bool = None):
        """
        Lista tareas para un usuario específico, opcionalmente filtradas por estado.
        :param usuario_id: ID del usuario.
        :param estado: Si es True, lista solo completadas; si es False, solo pendientes; si es None, todas.
        :return: Lista de objetos Tarea.
        """
        # Las funciones del repositorio ahora requieren la sesión
        return obtener_tareas_por_usuario(self.session, usuario_id, estado)

    def obtener_por_id(self, tarea_id: str):
        """Obtiene una tarea por su ID."""
        return obtener_tarea_por_id(self.session, tarea_id)

    def actualizar_tarea_con_subtareas(self, tarea_id: str, datos_a_actualizar: dict, 
                                     subtareas_data: list = None, etiquetas_str: str = "") -> bool:
        """
        Actualiza una tarea existente, sus subtareas y sus etiquetas.
        :param tarea_id: ID de la tarea a actualizar.
        :param datos_a_actualizar: Diccionario con los campos de la tarea principal a actualizar.
        :param subtareas_data: Lista de diccionarios con datos de subtareas (título, completada).
                                Si es None, no se modifican las subtareas.
        :param etiquetas_str: Cadena de texto con nombres de etiquetas separados por comas.
        :return: True si la tarea se actualizó exitosamente, False en caso contrario.
        """
        try:
            tarea = obtener_tarea_por_id(self.session, tarea_id)
            if not tarea:
                return False

            # Manejar etiquetas primero para que estén listas para la tarea
            etiquetas_para_tarea = []
            if etiquetas_str:
                nombres_etiquetas = [name.strip() for name in etiquetas_str.split(',') if name.strip()]
                for nombre in nombres_etiquetas:
                    etiqueta_obj = self.etiqueta_service.get_or_create_etiqueta(nombre)
                    etiquetas_para_tarea.append(etiqueta_obj)
            
            # Actualizar los datos de la tarea principal, incluyendo las etiquetas preparadas
            datos_a_actualizar['etiquetas'] = etiquetas_para_tarea # Añadir las etiquetas al diccionario para el repositorio
            actualizar_tarea(self.session, tarea_id, **datos_a_actualizar)

            # Manejar subtareas: Eliminar las existentes y crear las nuevas
            if subtareas_data is not None: # Si se proporciona, significa que queremos actualizar
                # Primero, eliminar todas las subtareas existentes para esta tarea
                # Obtener las subtareas actuales dentro de la misma sesión para evitar LazyLoadError
                current_subtasks = list(tarea.subtareas) # Copia la lista para evitar problemas al modificarla
                for existing_subtarea in current_subtasks:
                    eliminar_subtarea(self.session, existing_subtarea.subtarea_id) # Pasa la sesión, ✅ CORRECCIÓN: usar subtarea_id

                # Luego, insertar las nuevas subtareas
                for sub_data in subtareas_data:
                    nueva_subtarea = Subtarea(
                        subtarea_id=str(uuid.uuid4()), # ✅ CORRECCIÓN: Usar 'subtarea_id'
                        titulo=sub_data['titulo'],
                        descripcion=sub_data.get('descripcion', ''),
                        completada=sub_data.get('completada', False),
                        tarea_id=tarea_id
                    )
                    insertar_subtarea(self.session, nueva_subtarea.subtarea_id, nueva_subtarea.titulo, # Pasa la sesión, ✅ CORRECCIÓN: usar subtarea_id
                                      nueva_subtarea.descripcion, nueva_subtarea.completada,
                                      nueva_subtarea.tarea_id)

            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar tarea: {e}")
            return False

    def eliminar_tarea(self, tarea_id: str) -> bool:
        """Elimina una tarea por su ID."""
        try:
            eliminar_tarea_por_id(self.session, tarea_id)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error al eliminar tarea: {e}")
            return False

    def actualizar_estado_tarea(self, tarea_id: str, estado: bool) -> bool:
        """Actualiza el estado de una tarea (completada/pendiente)."""
        try:
            tarea = obtener_tarea_por_id(self.session, tarea_id)
            if tarea:
                tarea.estado = estado
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error al actualizar estado de tarea: {e}")
            return False
