import unittest
from faker import Faker
from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.cancion import Cancion
from src.modelo.interprete import Interprete
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
        self.cancion_prueba = Cancion(titulo="Canción de Prueba")
        self.session.add(self.cancion_prueba)
        self.interprete_prueba = Interprete(nombre="Intérprete de Prueba")
        self.session.add(self.interprete_prueba)
        self.session.commit()

    def tearDown(self):
        self.session.query(Album).delete()
        self.session.query(Cancion).delete()
        self.session.query(Interprete).delete()
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
        
    def test_eliminar_album_excepcion(self, mock_session):
        mock_session.query.side_effect = Exception("Error de prueba")

        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_album(1)
        
        self.assertEqual(str(context.exception), "Error de prueba")
        
    def test_eliminar_cancion_existente(self):
        cancion_id = self.cancion_prueba.id
        consulta = self.session.query(Cancion).filter(Cancion.id == cancion_id).first()
        self.assertIsNotNone(consulta)

        resultado = self.coleccion.eliminar_cancion(cancion_id)
        self.assertTrue(resultado)

        consulta = self.session.query(Cancion).filter(Cancion.id == cancion_id).first()
        self.assertIsNone(consulta)

    def test_eliminar_cancion_inexistente(self):
        resultado = self.coleccion.eliminar_cancion(99999)  # Usar un ID que no exista en la base de datos
        self.assertFalse(resultado)

    def test_eliminar_cancion_excepcion(self, mock_session):
        mock_session.query.side_effect = Exception("Error de prueba")

        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_cancion(self.cancion_prueba.id)
        
        self.assertEqual(str(context.exception), "Error de prueba")
        
    def test_eliminar_interprete_existente(self):
        interprete_id = self.interprete_prueba.id
        consulta = self.session.query(Interprete).filter(Interprete.id == interprete_id).first()
        self.assertIsNotNone(consulta)

        resultado = self.coleccion.eliminar_interprete(interprete_id)
        self.assertTrue(resultado)

        consulta = self.session.query(Interprete).filter(Interprete.id == interprete_id).first()
        self.assertIsNone(consulta)

    def test_eliminar_interprete_inexistente(self):
        interprete_id = 99999  # Usar un ID que no exista en la base de datos
        resultado = self.coleccion.eliminar_interprete(interprete_id)
        self.assertFalse(resultado)

    def test_eliminar_interprete_excepcion(self, mock_session):
        mock_session.query.side_effect = Exception("Error de prueba")

        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_interprete(self.interprete_prueba.id)
        
        self.assertEqual(str(context.exception), "Error de prueba")
