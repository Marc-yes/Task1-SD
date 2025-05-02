import Pyro4

@Pyro4.expose
class InsultFilter(object):
    def __init__(self, insult_service_uri):
        self.results = []  # Lista de resultados filtrados
        self.insult_service = Pyro4.Proxy(insult_service_uri)  # Proxy del servicio InsultService

    def notify(self, insult_list):
        """Recibir la lista de insultos del InsultService sin hacer nada con ella"""
        print(f"Received insult list: {insult_list}")
        self.insults = insult_list  # Almacenar la lista de insultos

    def filter_text(self, text):
        """Recibir un texto y censurarlo si contiene insultos"""
        insults = self.insult_service.get_insults()  # Obtener la lista de insultos actualizada
        censored_text = text
        
        # Censurar los insultos en el texto
        for insult in insults:
            censored_text = censored_text.replace(insult, "CENSORED")
        
        print(f"Filtered text: {censored_text}")
        self.results.append(censored_text)
        return censored_text

    def get_results(self):
        """Devolver los textos censurados"""
        return self.results


def main():
    daemon = Pyro4.Daemon()  # Crea el servidor Pyro
    ns = Pyro4.locateNS()  # Conecta al NameServer
    insult_service_uri = ns.lookup("insultservice")  # Obtiene la URI del InsultService registrado
    filter_service = InsultFilter(insult_service_uri)  # Crea la instancia del servicio InsultFilter
    uri = daemon.register(filter_service)  # Registra el objeto en Pyro
    ns.register("insultfilter", uri)  # Registra con el NameServer
    print(f"InsultFilter is running at {uri}")

    daemon.requestLoop()  # Mantiene el servicio ejecutándose

if __name__ == "__main__":
    main()
