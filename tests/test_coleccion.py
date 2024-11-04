import unittest
from faker import Faker
from src.logica.coleccion import Coleccion
from src.modelo.album import Album
from src.modelo.cancion import Cancion
from src.modelo.interprete import Interprete
from src.modelo.album import Album
from src.modelo.declarative_base import Session, Base, engine
from unittest.mock import patch


class ColeccionTestCase(unittest.TestCase):

    def setUp(self):
        self.session = Session()
        self.coleccion = Coleccion()

        Base.metadata.create_all(engine)
        
        # Agregar un intérprete de prueba
        self.interprete_prueba = Interprete(nombre="Intérprete de Prueba")
        self.session.add(self.interprete_prueba)
        self.session.commit()
        # Agregar un álbum de prueba
        self.album_prueba = Album(titulo="Álbum de Prueba")
        self.session.add(self.album_prueba)
        self.session.commit()
        # Agregar una canción de prueba
        self.cancion_prueba = Cancion(titulo="Canción de Prueba", albumes=[self.album_prueba])
        self.session.add(self.cancion_prueba)
        self.session.commit()
        self.cancion_prueba_2 = Cancion(titulo="Canción de Prueba 2", albumes=[self.album_prueba])
        self.session.add(self.cancion_prueba_2)
        self.session.commit()

    def test_eliminar_interprete_excepcion(self):
        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_interprete(9999)  # ID que sabemos que no existe
       
        self.assertEqual(str(context.exception), "Intérprete no encontrado.")
        
    def test_eliminar_album_excepcion(self):
        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_album(9999)  # ID que sabemos que no existe
        
        self.assertEqual(str(context.exception), "Álbum no encontrado.")
        
    def test_eliminar_cancion_excepcion(self):
        with self.assertRaises(Exception) as context:
            self.coleccion.eliminar_cancion(9999)
            
        self.assertEqual(str(context.exception), "Canción no encontrada.")
        
    def test_dar_canciones_de_album_exitoso(self):
        """Prueba exitosa de dar canciones de un álbum existente."""
        canciones = self.coleccion.dar_canciones_de_album(self.album.id)
        self.assertEqual(len(canciones), 2)
        self.assertIn("Canción 1", [c["titulo"] for c in canciones])
        self.assertIn("Canción 2", [c["titulo"] for c in canciones])

    def test_dar_canciones_de_album_no_encontrado(self):
        """Prueba de manejo de error al buscar un álbum inexistente."""
        with self.assertRaises(ValueError) as context:
            self.coleccion.dar_canciones_de_album(999)  # ID que no existe
        self.assertEqual(str(context.exception), "Álbum no encontrado.")    
