import Pyro4

@Pyro4.expose
class Subscriber(object):
    def __init__(self):
        self.received_insults = []  # Lista para almacenar los insultos recibidos

    def notify(self, insult_list):
        """Este método será llamado cuando InsultService envíe la lista completa de insultos"""
        print(f"[Suscriptor] Lista de insultos recibida: {insult_list}")
        self.received_insults = insult_list  # Almacenar la lista de insultos recibida

    def get_received_insults(self):
        """Devuelve la lista de insultos que ha recibido el suscriptor"""
        return self.received_insults

def main():
    # Crear una instancia de un suscriptor
    subscriber = Subscriber()

    # Crear el daemon de Pyro
    daemon = Pyro4.Daemon()

    # Registrar el suscriptor en Pyro y obtener su URI
    subscriber_uri = daemon.register(subscriber)
    print(f"URI del suscriptor: {subscriber_uri}")

    # Conectar al NameServer para obtener la URI de InsultService
    ns = Pyro4.locateNS()

    try:
        # Obtener la URI del InsultService desde el NameServer
        insult_service_uri = ns.lookup("insultservice_1")  # Asegúrate de que "insultservice_1" coincida con el nombre del servicio
        insult_service = Pyro4.Proxy(insult_service_uri)

        # Suscribir al suscriptor a InsultService
        insult_service.subscribe(subscriber_uri)
        print(f"Suscriptor suscrito a: {insult_service_uri}")

        # Mantener el daemon en ejecución para recibir insultos
        print("El suscriptor está recibiendo insultos...")
        daemon.requestLoop()

    except Pyro4.errors.CommunicationError as e:
        print(f"Error de comunicación: No se pudo conectar con InsultService - {e}")
    except Pyro4.errors.NamingError as e:
        print(f"Error de nombres: No se encontró InsultService en el NameServer - {e}")
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")

if __name__ == "__main__":
    main()
