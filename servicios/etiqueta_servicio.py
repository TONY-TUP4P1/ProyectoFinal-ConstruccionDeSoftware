from sqlalchemy.orm import Session
from modelos.etiqueta import Etiqueta
from repositorios.etiqueta_repositorio import EtiquetaRepository

class EtiquetaService:
    def __init__(self, session: Session):
        self.repo = EtiquetaRepository(session)

    def asignar_etiqueta(self, etiqueta: Etiqueta):
        self.repo.create(etiqueta)

    def eliminar_etiqueta(self, etiqueta_id: str):
        self.repo.delete(etiqueta_id)
