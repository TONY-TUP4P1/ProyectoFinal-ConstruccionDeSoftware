from sqlalchemy.orm import Session
from modelos.tarea import Tarea

class TareaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, tarea: Tarea):
        self.session.add(tarea)
        self.session.commit()

    def read(self, tarea_id: str):
        return self.session.query(Tarea).filter_by(id=tarea_id).first()

    def update(self, tarea: Tarea):
        self.session.commit()

    def delete(self, tarea_id: str):
        tarea = self.read(tarea_id)
        if tarea:
            self.session.delete(tarea)
            self.session.commit()
