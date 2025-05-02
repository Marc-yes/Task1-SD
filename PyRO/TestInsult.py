import unittest
import time
import Pyro4

# Definir el Cliente (Suscriptor) para recibir los insultos
@Pyro4.expose
class Subscriber(object):
    def __init__(self):
        self.received_insults = []

    def notify(self, insult):
        print(f"[Subscriber] Received insult: {insult}")
        self.received_insults.append(insult)

class TestInsultServiceAndFilter(unittest.TestCase):

    def setUp(self):
        """Configurar el entorno para el test"""
        self.subscriber = Subscriber()

        # Crear una instancia de InsultService y registrar al subscriber
        self.daemon = Pyro4.Daemon()
        self.ns = Pyro4.locateNS()

        # Registrar el subscriber en Pyro4 y obtener su URI
        subscriber_uri = self.daemon.register(self.subscriber)  # Registrar el Subscriber
        print(f"Subscriber URI: {subscriber_uri}")  # Para verificar que la URI está bien

        # Obtener la URI del InsultService
        self.insult_service_uri = self.ns.lookup("insultservice")
        self.insult_service = Pyro4.Proxy(self.insult_service_uri)

        # Suscribir al cliente (subscriber) usando su URI registrada
        self.insult_service.subscribe(subscriber_uri)

        # Crear una instancia de InsultFilter con la URI del InsultService
        self.filter_service = Pyro4.Proxy(self.ns.lookup("insultfilter"))

    def test_add_insult(self):
        """Verificar que el InsultService agregue insultos correctamente"""
        result = self.insult_service.add_insult("gilipollas")
        self.assertTrue(result)
        result = self.insult_service.add_insult("gilipollas")  # Intentar agregar el mismo insulto
        self.assertFalse(result)

    def test_broadcast_insults(self):
        """Verificar que los insultos sean enviados a los suscriptores cada 5 segundos"""
        self.insult_service.add_insult("tonto")
        self.insult_service.add_insult("idiota")
        
        # Esperar unos segundos para asegurarse de que los insultos sean enviados
        time.sleep(6)  # Ajustar el tiempo según el intervalo de envío (5 segundos)

        # Verificar que los insultos han sido recibidos por el subscriber
        self.assertGreater(len(self.subscriber.received_insults), 0)
        print(f"Insults received by subscriber: {self.subscriber.received_insults}")

    def test_filter_text(self):
        """Verificar que el InsultFilter pueda censurar los insultos en un texto"""
        self.insult_service.add_insult("tonto")
        self.insult_service.add_insult("idiota")

        # Texto con insultos
        text = "Eres un tonto y un idiota"
        
        # Procesar el texto usando InsultFilter
        censored_text = self.filter_service.filter_text(text)
        
        # Verificar que el texto fue censurado correctamente
        self.assertEqual(censored_text, "Eres un CENSORED y un CENSORED")

    def tearDown(self):
        """Limpiar después de las pruebas"""
        self.daemon.shutdown()  # Cerrar el servidor Pyro


if __name__ == "__main__":
    unittest.main()
