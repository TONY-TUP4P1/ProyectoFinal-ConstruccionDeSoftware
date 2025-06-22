import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.base import Base
from repositorios.subtarea_repositorio import SubtareaRepositorio
from repositorios.tarea_repositorio import TareaRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio
from servicios.subtarea_servicio import SubtareaServicio
from servicios.tarea_servicio import TareaServicio
from servicios.usuario_servicio import UsuarioServicio


class TestSubtareaServicio(unittest.TestCase):
    def setUp(self):
        engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(engine)
        self.session = sessionmaker(bind=engine)()

        self.usuario_repo = UsuarioRepositorio(self.session)
        self.tarea_repo = TareaRepositorio(self.session)
        self.subtarea_repo = SubtareaRepositorio(self.session)

        self.usuario_servicio = UsuarioServicio(self.usuario_repo)
        self.tarea_servicio = TareaServicio(self.tarea_repo, self.usuario_repo)
        self.subtarea_servicio = SubtareaServicio(
            self.subtarea_repo, self.tarea_repo)

        self.usuario = self.usuario_servicio.registrar_usuario(
            "Ana", "Campos", "ana@example.com", "clave123"
        )

        self.tarea = self.tarea_servicio.crear_tarea(
            usuario_id=self.usuario.id,
            titulo="Tarea principal"
        )

    def test_crear_subtarea(self):
        subtarea = self.subtarea_servicio.crear_subtarea(
            tarea_id=self.tarea.id,
            titulo="Paso 1"
        )
        self.assertEqual(subtarea.titulo, "Paso 1")

    def test_crear_subtarea_sin_titulo(self):
        with self.assertRaises(ValueError):
            self.subtarea_servicio.crear_subtarea(
                tarea_id=self.tarea.id, titulo="")

    def test_tarea_inexistente(self):
        with self.assertRaises(ValueError):
            self.subtarea_servicio.crear_subtarea(
                tarea_id="nula", titulo="Hola")

    def tearDown(self):
        self.session.close()



if __name__ == "__main__":
    unittest.main()
