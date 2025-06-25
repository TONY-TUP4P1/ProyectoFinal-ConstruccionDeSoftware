from sqlalchemy.orm import Session
from modelos.categoria import Categoria

class CategoriaRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, categoria: Categoria):
        self.session.add(categoria)
        self.session.commit()

    def read(self, categoria_id: str):
        return self.session.query(Categoria).filter_by(id=categoria_id).first()

    def update(self, categoria: Categoria):
        self.session.commit()

    def delete(self, categoria_id: str):
        categoria = self.read(categoria_id)
        if categoria:
            self.session.delete(categoria)
            self.session.commit()
