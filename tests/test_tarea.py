import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from modelos.base import Base
from repositorios.tarea_repositorio import TareaRepositorio
from repositorios.usuario_repositorio import UsuarioRepositorio
from servicios.tarea_servicio import TareaServicio
from servicios.usuario_servicio import UsuarioServicio


class TestTareaServicio(unittest.TestCase):
    def setUp(self):
        self.engine = create_engine("sqlite:///:memory:")
        Base.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

        self.usuario_repo = UsuarioRepositorio(self.session)
        self.tarea_repo = TareaRepositorio(self.session)

        self.usuario_servicio = UsuarioServicio(self.usuario_repo)
        self.tarea_servicio = TareaServicio(self.tarea_repo, self.usuario_repo)

        self.usuario = self.usuario_servicio.registrar_usuario(
            "Test", "User", "testuser@example.com", "pass"
        )

    def test_crear_tarea(self):
        tarea = self.tarea_servicio.crear_tarea(
            usuario_id=self.usuario.id,
            titulo="Mi primera tarea",
            descripcion="Descripción de tarea",
            fecha_limite=datetime(2025, 12, 31)
        )
        self.assertEqual(tarea.titulo, "Mi primera tarea")

    def test_tarea_sin_titulo(self):
        with self.assertRaises(ValueError):
            self.tarea_servicio.crear_tarea(
                usuario_id=self.usuario.id,
                titulo=""
            )

    def test_usuario_no_existente(self):
        with self.assertRaises(ValueError):
            self.tarea_servicio.crear_tarea(
                usuario_id="invalido", titulo="Tarea inválida"
            )

    def tearDown(self):
        self.session.close()
        self.engine.dispose()



if __name__ == "__main__":
    unittest.main()
