import Pyro4
import random
import time
import threading
from multiprocessing import Process

@Pyro4.expose
class InsultService:
    def __init__(self, service_name):
        self.insults = set()
        self.subscribers = []  # Lista para los suscriptores
        self.insult_filter_uri = None  # URI del filtro (sin instancia directa)
        self.running = True
        self.service_name = service_name
        threading.Thread(target=self._broadcast_insults, daemon=True).start()  # Hilo para la transmisión de insultos

    def add_insult(self, insult):
        """Recibe un insulto y lo agrega a la lista si no está ya presente"""
        if insult not in self.insults:
            print(f"[{self.service_name}] Adding insult: {insult}")
            self.insults.add(insult)
            return True
        return False

    def get_insults(self):
        """Devuelve la lista de insultos"""
        return list(self.insults)

    def subscribe(self, subscriber_uri):
        """Permite a un cliente (suscriptor) registrarse para recibir insultos"""
        print(f"[{self.service_name}] New subscriber: {subscriber_uri}")
        subscriber = Pyro4.Proxy(subscriber_uri)
        self.subscribers.append(subscriber)
        return True

    def set_insult_filter(self, insult_filter_uri):
        """Recibe la URI del InsultFilter y la almacena para usarse más tarde"""
        self.insult_filter_uri = insult_filter_uri
        print(f"[{self.service_name}] Set InsultFilter URI: {self.insult_filter_uri}")

    def pass_insults_to_filter(self):
        """Pasa los insultos a InsultFilter"""
        if self.insult_filter_uri:
            # Conectamos al InsultFilter usando su URI
            insult_filter = Pyro4.Proxy(self.insult_filter_uri)
            insults = self.get_insults()  # Obtener insultos
            insult_filter.receive_insults(insults)  # Enviar insultos a InsultFilter
        else:
            print("No InsultFilter set! Cannot pass insults.")

    def filter_text(self, text):
        """Filtra el texto utilizando el InsultFilter"""
        if self.insult_filter_uri:
            insult_filter = Pyro4.Proxy(self.insult_filter_uri)
            censored_text = insult_filter.filter_text(text)
            return censored_text
        return text

    def _broadcast_insults(self):
        """Difunde la lista completa de insultos a los suscriptores cada 5 segundos"""
        while self.running:
            if self.insults and self.subscribers:
                insult_list = list(self.insults)
                print(f"[{self.service_name}] Sending insult list: {insult_list}")  # Imprimir lista completa para verificación
                for sub in self.subscribers:
                    try:
                        sub.notify(insult_list)  # Notificar a cada suscriptor con la lista completa de insultos
                    except Exception as e:
                        print(f"Subscriber error: {e}")
            else:
                print(f"[{self.service_name}] No insults or no subscribers. Waiting...")  # Mensaje si no hay insultos o suscriptores
            time.sleep(5)  # Espera de 5 segundos antes de volver a enviar la lista


def run_service(service_name):
    """Función para iniciar el servicio InsultService en un nuevo proceso"""
    daemon = Pyro4.Daemon()  # Crea el servidor Pyro
    ns = Pyro4.locateNS()  # Conecta al NameServer

    # Crear y registrar el servicio con un nombre único por servicio
    service = InsultService(service_name)
    uri = daemon.register(service)  # Registrar el objeto en Pyro
    ns.register(service_name, uri)  # Registrar con el NameServer

    print(f"{service_name} is running.")
    print(f"URI: {uri}")  # Verifica la URI en la que el servicio está registrado

    daemon.requestLoop()  # Mantiene el servicio ejecutándose


def main():
    """Inicia múltiples nodos (servicios) en paralelo"""
    # Crear diferentes nodos con nombres únicos
    service_names = ["insultservice_1", "insultservice_2", "insultservice_3"]

    # Usamos multiprocessing para ejecutar los servicios en paralelo
    processes = []
    for name in service_names:
        p = Process(target=run_service, args=(name,))
        processes.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
