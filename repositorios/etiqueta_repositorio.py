from sqlalchemy.orm import Session
from modelos.etiqueta import Etiqueta

class EtiquetaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, etiqueta: Etiqueta):
        self.session.add(etiqueta)
        self.session.commit()

    def read(self, etiqueta_id: str):
        return self.session.query(Etiqueta).filter_by(id=etiqueta_id).first()

    def update(self, etiqueta: Etiqueta):
        self.session.commit()

    def delete(self, etiqueta_id: str):
        etiqueta = self.read(etiqueta_id)
        if etiqueta:
            self.session.delete(etiqueta)
            self.session.commit()
