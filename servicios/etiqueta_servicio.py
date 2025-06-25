from sqlalchemy.orm import Session
from modelos.etiqueta import Etiqueta
# Importar todas las funciones del repositorio directamente para usarlas con la sesión
from repositorios.etiqueta_repositorio import (
    insertar_etiqueta,
    obtener_etiquetas,
    actualizar_etiqueta,
    eliminar_etiqueta,
    obtener_etiqueta_por_nombre # Nueva función
)
import uuid # Para generar IDs para nuevas etiquetas

class EtiquetaService:
    def __init__(self, session: Session):
        self.session = session

    def crear_etiqueta(self, etiqueta: Etiqueta):
        """Crea una nueva etiqueta."""
        insertar_etiqueta(self.session, etiqueta.etiqueta_id, etiqueta.nombre)
        self.session.commit() # Commit handled by service

    def listar_etiquetas(self):
        """Lista todas las etiquetas."""
        return obtener_etiquetas(self.session)

    def actualizar_etiqueta(self, etiqueta_id: str, nuevo_nombre: str):
        """Actualiza el nombre de una etiqueta existente."""
        actualizar_etiqueta(self.session, etiqueta_id, nuevo_nombre)
        self.session.commit() # Commit handled by service

    def eliminar_etiqueta(self, etiqueta_id: str):
        """Elimina una etiqueta por su ID."""
        eliminar_etiqueta(self.session, etiqueta_id)
        self.session.commit() # Commit handled by service

    def get_or_create_etiqueta(self, nombre_etiqueta: str) -> Etiqueta:
        """
        Obtiene una etiqueta existente por su nombre o crea una nueva si no existe.
        """
        etiqueta = obtener_etiqueta_por_nombre(self.session, nombre_etiqueta)
        if not etiqueta:
            # Crea una nueva etiqueta si no existe
            etiqueta_id = str(uuid.uuid4())
            etiqueta = Etiqueta(etiqueta_id=etiqueta_id, nombre=nombre_etiqueta)
            self.session.add(etiqueta)
            # No commit here, as it might be part of a larger transaction
            # The calling service (TareaService) will commit.
        return etiqueta
