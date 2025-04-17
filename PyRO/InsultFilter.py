import Pyro4

@Pyro4.expose
class InsultFilter(object):
    def __init__(self, insult_service_uri):
        self.results = []
        self.insult_service = Pyro4.Proxy(insult_service_uri)

    def filter_text(self, text):
        insults = self.insult_service.get_insults()
        censored_text = text
        for insult in insults:
            censored_text = censored_text.replace(insult, "CENSORED")
        print(f"Filtered text: {censored_text}")
        self.results.append(censored_text)
        return censored_text

    def get_results(self):
        return self.results


def main():
    daemon = Pyro4.Daemon()  # Crea el servidor
    ns = Pyro4.locateNS()  # Conecta al NameServer
    insult_service_uri = ns.lookup("insultservice")  # Obtiene la URI del InsultService registrado
    filter_service = InsultFilter(insult_service_uri)  # Crea el servicio InsultFilter
    uri = daemon.register(filter_service)  # Registra el objeto
    ns.register("insultfilter", uri)  # Registra con el NameServer
    print(f"InsultFilter is running at {uri}")

    daemon.requestLoop()  # Mantiene el servicio ejecutándose

if __name__ == "__main__":
    main()
