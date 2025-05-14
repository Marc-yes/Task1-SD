import unittest
from unittest.mock import MagicMock
import Pyro4
import time

# Importa las clases que queremos probar
from InsultService import InsultService
from Subscriber import Subscriber

class TestInsultService(unittest.TestCase):

    def setUp(self):
        """Configura el entorno para cada prueba"""
        # Crear la instancia de InsultService
        self.insult_service = InsultService()

        # Crear el daemon de Pyro
        self.daemon = Pyro4.Daemon()

        # Crear un mock del suscriptor y sobrescribir el método `notify`
        self.mock_subscriber = MagicMock(spec=Subscriber)  # Crear un mock del tipo Subscriber
        self.mock_subscriber_uri = self.daemon.register(self.mock_subscriber)  # Registrar el mock del suscriptor
        print(f"Subscriber URI: {self.mock_subscriber_uri}")  # Verificar la URI

        # Registrar el InsultService en Pyro y obtener su URI real
        self.insult_service_uri = self.daemon.register(self.insult_service)  # Registrar el InsultService
        print(f"InsultService URI: {self.insult_service_uri}")  # Verificar la URI

        # Conectar al NameServer para registrar el servicio
        self.ns = Pyro4.locateNS()
        self.ns.register("insultservice", self.insult_service_uri)

        # Suscribir el mock del suscriptor a InsultService usando su URI real
        self.insult_service.subscribe(self.mock_subscriber_uri)

    def test_add_insult(self):
        """Verificar que se pueda agregar un insulto"""
        result = self.insult_service.add_insult("tonto")
        self.assertTrue(result)
        result = self.insult_service.add_insult("tonto")  # Intentar agregar el mismo insulto
        self.assertFalse(result)

    def test_get_insults(self):
        """Verificar que se pueda obtener la lista de insultos"""
        self.insult_service.add_insult("tonto")
        insults = self.insult_service.get_insults()
        self.assertEqual(insults, ["tonto"])

    def test_subscribe(self):
        """Verificar que un suscriptor se pueda registrar correctamente"""
        self.insult_service.add_insult("idiota")
        self.insult_service.add_insult("tonto")

        # Ejecutar la transmisión de insultos por 6 segundos
        time.sleep(6)  # Deja que el hilo de transmisión se ejecute un poco más tiempo

        # Verificar si el suscriptor ha sido añadido a la lista de suscriptores
        self.assertIn(self.mock_subscriber_uri, self.insult_service.subscribers)

    def test_broadcast_insults(self):
        """Verificar que se envíen los insultos a los suscriptores cada 5 segundos"""
        self.insult_service.add_insult("tonto")
        self.insult_service.add_insult("idiota")

        # Ejecutar la transmisión de insultos por 6 segundos (más que suficiente para que se envíen al menos una vez)
        time.sleep(6)

        # Verificar que el suscriptor haya recibido los insultos
        received_insults = self.mock_subscriber.notify.call_args_list
        print(f"Received insults: {received_insults}")

        # Verificar que el suscriptor haya recibido la lista completa de insultos
        self.assertIn(["tonto", "idiota"], [args[0] for args in received_insults])

    def tearDown(self):
        """Limpiar después de las pruebas"""
        self.daemon.shutdown()  # Cerrar el servidor Pyro

if __name__ == "__main__":
    unittest.main()
