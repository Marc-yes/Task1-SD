import unittest
import time
from unittest.mock import MagicMock
from InsultService import InsultService

class TestInsultService(unittest.TestCase):

    def setUp(self):
        # Crear el servicio InsultService con test_mode=True para evitar que se quede bloqueado
        self.service = InsultService(test_mode=True)  # Activar test_mode para evitar el bucle infinito
        self.service.channel = MagicMock()  # Usar un mock para el canal de RabbitMQ

    def test_add_insult(self):
        """Verificar que se puede agregar un insulto"""
        result = self.service.add_insult("gilipollas")
        self.assertTrue(result)  # 'gilipollas' es nuevo

        result = self.service.add_insult("gilipollas")
        self.assertFalse(result)  # 'gilipollas' ya existe

    def test_broadcast_insults_once(self):
        """Verificar que los insultos se envían correctamente una sola vez"""
        self.service.insults = {"tonto", "idiota"}
        
        # Ejecutar una vez el broadcast
        self.service.broadcast_insults_once()  # Solo ejecutará una vez debido a test_mode=True
        
        # Verificar que se haya llamado a basic_publish con el mensaje correcto
        self.service.channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='insult_queue',
            body="tonto,idiota"
        )

    def test_process_text(self):
        """Verificar que el texto enviado se publica correctamente en la cola"""
        text = "Eres un tonto"
        self.service.process_text(text)
        
        # Verificar que el texto fue publicado correctamente en la cola 'text_queue'
        self.service.channel.basic_publish.assert_called_once_with(
            exchange='',
            routing_key='text_queue',
            body=text
        )

if __name__ == '__main__':
    unittest.main()
