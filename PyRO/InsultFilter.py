import Pyro4
import threading
from multiprocessing import Process


@Pyro4.expose
class InsultFilter:
    def __init__(self, filter_name):
        self.insults = []  # Lista de insultos
        self.filter_name = filter_name  # Nombre único para cada nodo

    def receive_insults(self, insult_list):
        """Recibe los insultos de InsultService"""
        self.insults = insult_list
        print(f"[{self.filter_name}] InsultFilter received insults: {self.insults}")

    def filter_text(self, text):
        """Filtra el texto según los insultos recibidos"""
        censored_text = text
        if not self.insults:
            print(f"[{self.filter_name}] No insults to filter.")
            return text  # Si no hay insultos, retorna el texto original.

        for insult in self.insults:
            censored_text = censored_text.replace(insult, "CENSORED")
        print(f"[{self.filter_name}] Filtered text: {censored_text}")
        return censored_text


def run_insult_filter(filter_name):
    """Función para iniciar el nodo de InsultFilter en un nuevo proceso"""
    daemon = Pyro4.Daemon()  # Crea el servidor Pyro
    ns = Pyro4.locateNS()  # Conecta al NameServer

    # Crear y registrar el servicio con un nombre único por nodo
    insult_filter = InsultFilter(filter_name)
    uri = daemon.register(insult_filter)  # Registrar el objeto en Pyro
    ns.register(filter_name, uri)  # Registrar con el NameServer

    print(f"[{filter_name}] InsultFilter is running.")
    print(f"URI: {uri}")  # Verifica la URI en la que el servicio está registrado

    daemon.requestLoop()  # Mantiene el servicio ejecutándose


def main():
    """Inicia hasta tres nodos de InsultFilter en paralelo"""
    filter_names = ["insultfilter_1", "insultfilter_2", "insultfilter_3"]

    # Usamos multiprocessing para ejecutar los servicios en paralelo
    processes = []
    for name in filter_names:
        p = Process(target=run_insult_filter, args=(name,))
        processes.append(p)
        p.start()

    # Esperar a que todos los procesos terminen
    for p in processes:
        p.join()

if __name__ == "__main__":
    main()
