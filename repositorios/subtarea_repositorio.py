from sqlalchemy.orm import Session
from modelos.subtarea import SubTarea

class SubTareaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, subtarea: SubTarea):
        self.session.add(subtarea)
        self.session.commit()

    def read(self, subtarea_id: str):
        return self.session.query(SubTarea).filter_by(id=subtarea_id).first()

    def update(self, subtarea: SubTarea):
        self.session.commit()

    def delete(self, subtarea_id: str):
        subtarea = self.read(subtarea_id)
        if subtarea:
            self.session.delete(subtarea)
            self.session.commit()
