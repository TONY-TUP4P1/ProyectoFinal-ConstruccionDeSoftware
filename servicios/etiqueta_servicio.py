from modelos.etiqueta import Etiqueta
from repositorios.etiqueta_repositorio import EtiquetaRepositorio


class EtiquetaServicio:
    def __init__(self, etiqueta_repo: EtiquetaRepositorio):
        self.etiqueta_repo = etiqueta_repo

    def crear_etiqueta(self, nombre: str):
        if not nombre:
            raise ValueError("El nombre de la etiqueta es obligatorio.")
        if self.etiqueta_repo.obtener_por_nombre(nombre):
            raise ValueError("La etiqueta ya existe.")
        nueva_etiqueta = Etiqueta(nombre=nombre)
        return self.etiqueta_repo.crear(nueva_etiqueta)

    def listar_etiquetas(self):
        return self.etiqueta_repo.listar()

    def obtener_etiqueta(self, etiqueta_id: str):
        etiqueta = self.etiqueta_repo.obtener_por_id(etiqueta_id)
        if not etiqueta:
            raise ValueError("Etiqueta no encontrada.")
        return etiqueta
