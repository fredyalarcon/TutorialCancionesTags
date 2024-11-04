import unittest
from faker import Faker
from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.declarative_base import Session, Base, engine


class AlbumTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()
        
        Base.metadata.create_all(engine)
        # Instanciar Faker para generación de datos
        self.data_factory = Faker()

        self.album_prueba = Album(titulo="Álbum de Prueba")
        self.session.add(self.album_prueba)
        self.session.commit()

    def tearDown(self):
        self.session.query(Album).delete()
        self.session.commit()
        self.session.close()

    def test_eliminar_album_existente(self):
        album_id = self.album_prueba.id
        consulta = self.session.query(Album).filter(Album.id == album_id).first()
        self.assertIsNotNone(consulta)  # Confirmar que el álbum existe

        resultado = self.coleccion.eliminar_album(album_id)
        self.assertTrue(resultado)

        consulta = self.session.query(Album).filter(Album.id == album_id).first()
        self.assertIsNone(consulta)

    def test_eliminar_album_inexistente(self):
        resultado = self.coleccion.eliminar_album(99999)  # Un ID que no existe
        self.assertFalse(resultado)
